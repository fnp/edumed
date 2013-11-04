import random
import string

from django.db import models

from contact.models import Contact


class Submission(models.Model):
    contact = models.ForeignKey(Contact, null = True)
    key = models.CharField(max_length = 30, unique = True)
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    email = models.EmailField(max_length = 100, unique = True)
    answers = models.CharField(max_length = 65536, null = True, blank = True)

    @classmethod
    def generate_key(cls):
        key = ''
        while not key and key in [record['key'] for record in cls.objects.values('key')]:
            key = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(30))
        return key

    @classmethod
    def create(cls, first_name, last_name, email, contact = None, key = None):
        submissions = []

        if contact:
            students = contact['students']
        else:
            students = [dict(first_name = first_name, last_name = last_name, email = email)]
        
        if key is None:
            key = Submission.generate_key()

        for student in students:
            submission = cls(
                contact = contact,
                key = key,
                first_name = student['first_name'],
                last_name = student['last_name'],
                email = student['email']
            )
            submission.save()
            submissions.append(submission)
        return submissions


class Attachment(models.Model):
    submission = models.ForeignKey(Submission)
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to = 'wtem/attachment')