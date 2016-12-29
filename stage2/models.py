# -*- coding: utf-8 -*-
import os
import random
import string

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField

from contact.models import Contact


class Participant(models.Model):
    contact = models.ForeignKey(Contact, verbose_name=_('contact'), null=True)
    key = models.CharField(_('key'), max_length=30, unique=True)
    first_name = models.CharField(_('first name'), max_length=100)
    last_name = models.CharField(_('last_name'), max_length=100)
    email = models.EmailField(_('email'), max_length=100, unique=True)
    key_sent = models.BooleanField(_('key sent'), default=False)

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


class Assignment(models.Model):
    title = models.CharField(_('title'), max_length=128)
    content = models.TextField(_('content'))
    deadline = models.DateTimeField(_('deadline'))
    max_points = models.IntegerField(_('max points'))
    file_descriptions = JSONField(_('file descriptions'))

    class Meta:
        ordering = ['deadline']
        verbose_name = _('assignment')
        verbose_name_plural = _('assignments')

    def __unicode__(self):
        return self.title


class Answer(models.Model):
    participant = models.ForeignKey(Participant)
    assignment = models.ForeignKey(Assignment)

    class Meta:
        unique_together = ['participant', 'assignment']


def attachment_path(instance, filename):
    answer = instance.answer
    return 'stage2/attachment/%s/%s/%s' % (answer.participant_id, answer.assignment_id, filename)


class Attachment(models.Model):
    answer = models.ForeignKey(Answer)
    file_no = models.IntegerField()
    file = models.FileField(upload_to=attachment_path)

    def filename(self):
        return os.path.basename(self.file.name)

    def download_url(self):
        return reverse(
            'stage2_participant_file',
            args=(self.answer.assignment_id, self.file_no,
                  self.answer.participant_id, self.answer.participant.key))


class Mark(models.Model):
    expert = models.ForeignKey(User)
    answer = models.ForeignKey(Answer)
    points = models.DecimalField(max_digits=3, decimal_places=1)

    class Meta:
        unique_together = ['expert', 'answer']
