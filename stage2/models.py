# -*- coding: utf-8 -*-
import os
import random
import string

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
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
    file_descriptions = JSONField(_('file descriptions'))

    class Meta:
        ordering = ['deadline', 'title']
        verbose_name = _('assignment')
        verbose_name_plural = _('assignments')

    def __unicode__(self):
        return self.title

    def available_answers(self, expert):
        answers = self.answer_set.exclude(mark__expert=expert).filter(participant__complete_set=True)
        if expert not in self.supervisors.all():
            answers = answers.exclude(complete=True)
        if expert in self.arbiters.all():
            answers = answers.filter(need_arbiter=True)
        return answers

    def is_active(self):
        return self.deadline >= timezone.now()


class Answer(models.Model):
    participant = models.ForeignKey(Participant)
    assignment = models.ForeignKey(Assignment)
    # useful redundancy
    complete = models.BooleanField(default=False)
    need_arbiter = models.BooleanField(default=False)

    class Meta:
        unique_together = ['participant', 'assignment']

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