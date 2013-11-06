import random
import string

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from jsonfield import JSONField

from contact.models import Contact


DEBUG_KEY = '12345'

class Submission(models.Model):
    contact = models.ForeignKey(Contact, null = True)
    key = models.CharField(max_length = 30, unique = True)
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    email = models.EmailField(max_length = 100, unique = True)
    answers = models.CharField(max_length = 65536, null = True, blank = True)
    key_sent = models.BooleanField(default = False)

    @classmethod
    def generate_key(cls):
        key = ''
        while not key or key in [record['key'] for record in cls.objects.values('key')]:
            key = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(30))
        return key

    @classmethod
    def create(cls, first_name, last_name, email, key = None, contact = None):
        submission = cls(
            contact = contact,
            key = key if key else Submission.generate_key(),
            first_name = first_name,
            last_name = last_name,
            email = email
        )

        submission.save()
        return submission


class Attachment(models.Model):
    submission = models.ForeignKey(Submission)
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to = 'wtem/attachment')


class Assignment(models.Model):
    user = models.ForeignKey(User, unique = True)
    exercises = JSONField()

    def clean(self):
        if not isinstance(self.exercises, list):
            raise ValidationError(_('Assigned exercises must be declared in a list format'))
        for exercise in self.exercises:
            if not isinstance(exercise, int) or exercise < 1:
                raise ValidationError(_('Invalid exercise id: %s' % exercise))

    def __unicode__(self):
        return self.user.username + ': ' + ','.join(map(str,self.exercises))