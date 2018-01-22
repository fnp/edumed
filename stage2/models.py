# -*- coding: utf-8 -*-
import os
import random
import string

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from jsonfield import JSONField

from contact.models import Contact


class Participant(models.Model):
    contact = models.ForeignKey(Contact, verbose_name=_('contact'), null=True)
    key = models.CharField(_('key'), max_length=30, unique=True)
    first_name = models.CharField(_('first name'), max_length=100)
    last_name = models.CharField(_('last_name'), max_length=100)
    email = models.EmailField(_('email'), max_length=100, unique=True)
    key_sent = models.BooleanField(_('key sent'), default=False)
    complete_set = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('participant')
        verbose_name_plural = _('participants')

    def __unicode__(self):
        return ', '.join((self.last_name, self.first_name, self.email))

    # copy-paste from wtem
    @classmethod
    def generate_key(cls):
        key = ''
        while not key or key in [record['key'] for record in cls.objects.values('key')]:
            key = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
                          for i in range(30))
        return key

    # copy-paste from wtem
    @classmethod
    def create(cls, first_name, last_name, email, key=None, contact=None):
        return cls.objects.create(
            contact=contact,
            key=key if key else cls.generate_key(),
            first_name=first_name,
            last_name=last_name,
            email=email)

    def check(self, key):
        return key == self.key

    def score(self):
        return sum(answer.score() for answer in self.answer_set.all())


class Assignment(models.Model):
    title = models.CharField(_('title'), max_length=128)
    content = models.TextField(_('content'))
    content_url = models.URLField(_('URL'))
    deadline = models.DateTimeField(_('deadline'))
    max_points = models.IntegerField(_('max points'))
    experts = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name=_('experts'), related_name='stage2_assignments')
    arbiters = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, verbose_name=_('arbiters'), related_name='stage2_arbitrated')
    supervisors = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name=_('supervisors'), related_name='stage2_supervised')
    file_descriptions = JSONField(_('file descriptions'), default=[], blank=True)
    field_descriptions = JSONField(_('field descriptions'), default=[], blank=True)

    class Meta:
        ordering = ['deadline', 'title']
        verbose_name = _('assignment')
        verbose_name_plural = _('assignments')

    def __unicode__(self):
        return self.title

    def available_answers(self, expert):
        answers = self.answer_set.exclude(mark__expert=expert)
        assigned_to_expert = self.answer_set.filter(expert=expert).exists()
        is_supervisor = expert in self.supervisors.all()
        is_arbiter = expert in self.arbiters.all()
        if assigned_to_expert:
            expert_answers = answers.filter(expert=expert)
            if expert_answers or not is_arbiter:
                answers = expert_answers
        answers = answers.extra(where=[
            "field_values::text ~ ': *\"[^\"]+\"' "
            "OR EXISTS (SELECT id FROM stage2_attachment WHERE answer_id = stage2_answer.id) "
            "OR EXISTS (SELECT id FROM stage2_fieldoption WHERE answer_id = stage2_answer.id)"])
        if not is_supervisor:
            answers = answers.exclude(complete=True)
        if not is_supervisor or not self.is_active():
            answers = answers.filter(participant__complete_set=True)
        if is_arbiter:
            answers = answers.filter(need_arbiter=True)
        return answers

    def field_counts(self, answers):
        for field_desc in self.field_descriptions:
            field_name, params = field_desc
            if params['type'] == 'options':
                field_count = FieldOption.objects.filter(answer__in=list(answers), set__name=params['option_set']).count()
            else:  # text, link
                field_count = sum(1 for answer in answers if answer.field_values.get(field_name))
            yield field_name, field_count

    def is_active(self):
        return self.deadline >= timezone.now()


class Answer(models.Model):
    participant = models.ForeignKey(Participant)
    assignment = models.ForeignKey(Assignment)
    field_values = JSONField(_('field values'), default={})
    experts = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name=_('experts'), related_name='stage2_assigned_answers')
    # useful redundancy
    complete = models.BooleanField(default=False)
    need_arbiter = models.BooleanField(default=False)

    class Meta:
        unique_together = ['participant', 'assignment']

    def fields(self):
        for field_desc in self.assignment.field_descriptions:
            field_name, params = field_desc
            if params['type'] == 'options':
                option = self.fieldoption_set.filter(set__name=params['option_set'])
                value = option.get().value if option else '--------'
            else:  # text, link
                value = self.field_values.get(field_name, '')
            if params['type'] == 'link':
                value = format_html(u'<a href="{url}">{url}</a>', url=value)
            yield field_name, value

    def update_complete(self):
        marks = self.mark_set.all()
        if len(marks) < 2:
            complete = False
            need_arbiter = False
        elif len(marks) == 2:
            mark1, mark2 = marks
            complete = abs(mark1.points - mark2.points) < 0.2 * self.assignment.max_points
            need_arbiter = not complete
        else:
            complete = True
            need_arbiter = False
        self.complete = complete
        self.need_arbiter = need_arbiter
        self.save()

    def score(self):
        marks = self.mark_set.all()
        if len(marks) < 2:
            return None
        return self.mark_set.aggregate(avg=models.Avg('points'))['avg']

    # unrelated to `complete' attribute, but whatever
    def is_complete(self):
        file_count = len(self.assignment.file_descriptions)
        field_count = len(self.assignment.field_descriptions)
        if self.attachment_set.count() < file_count:
            return False
        if self.fieldoption_set.count() + sum(1 for k, v in self.field_values.iteritems() if v) < field_count:
            return False
        return True


class FieldOptionSet(models.Model):
    name = models.CharField(verbose_name=_('nazwa'), max_length=32, db_index=True)

    class Meta:
        verbose_name = _('option set')
        verbose_name_plural = _('option sets')

    def __unicode__(self):
        return self.name

    def choices(self, answer):
        return [('', '--------')] + [
            (option.id, option.value)
            for option in self.fieldoption_set.extra(
                where=['answer_id is null or answer_id = %s'],
                params=[answer.id])]


class FieldOption(models.Model):
    set = models.ForeignKey(FieldOptionSet, verbose_name=_('zestaw'))
    value = models.CharField(verbose_name=_('value'), max_length=255)
    answer = models.ForeignKey(Answer, verbose_name=_('answer'), null=True, blank=True)

    class Meta:
        ordering = ['set', 'value']
        verbose_name = _('option')
        verbose_name_plural = _('options')

    def __unicode__(self):
        return self.value


def attachment_path(instance, filename):
    answer = instance.answer
    return 'stage2/attachment/%s/%s/%s/%s' % (answer.participant_id, answer.assignment_id, instance.file_no, filename)


class Attachment(models.Model):
    answer = models.ForeignKey(Answer)
    file_no = models.IntegerField()
    file = models.FileField(upload_to=attachment_path)

    class Meta:
        ordering = ['file_no']

    def filename(self):
        return os.path.basename(self.file.name)

    def download_url(self):
        return reverse(
            'stage2_participant_file',
            args=(self.answer.assignment_id, self.file_no,
                  self.answer.participant_id, self.answer.participant.key))

    def expert_download_url(self):
        return reverse('stage2_expert_download', args=[self.id])


class Mark(models.Model):
    expert = models.ForeignKey(settings.AUTH_USER_MODEL)
    answer = models.ForeignKey(Answer)
    points = models.DecimalField(verbose_name=_('points'), max_digits=3, decimal_places=1)

    class Meta:
        unique_together = ['expert', 'answer']


@receiver(post_save, sender=Mark, dispatch_uid='update_answer')
def update_answer(sender, **kwargs):
    mark = kwargs['instance']
    mark.answer.update_complete()
