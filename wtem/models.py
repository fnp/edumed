# -*- coding: utf-8 -*-
import random
import string
import os
import json

from datetime import datetime

import pytz as pytz
from django.conf import settings
from django.core.validators import validate_email
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import ugettext as _
from jsonfield import JSONField

from contact.models import Contact

f = file(os.path.dirname(__file__) + '/fixtures/exercises.json')
exercises = json.loads(f.read())
f.close()

DEBUG_KEY = 'smerfetka159'

tz = pytz.timezone(settings.TIME_ZONE)


def get_exercise_by_id(exercise_id):
    return [e for e in exercises if str(e['id']) == str(exercise_id)][0]


def make_key(length):
    return ''.join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
        for i in range(length))


def tuple2dt(time_tuple):
    return tz.localize(datetime(*time_tuple))


class CompetitionState(models.Model):
    """singleton"""
    BEFORE = 'before'
    DURING = 'during'
    AFTER = 'after'
    STATE_CHOICES = (
        (BEFORE, u'przed rozpoczęciem'),
        (DURING, u'w trakcie'),
        (AFTER, u'po zakończeniu'),
    )
    state = models.CharField(choices=STATE_CHOICES, max_length=16)

    start = tuple2dt(settings.OLIMPIADA_START)
    end = tuple2dt(settings.OLIMPIADA_END)

    @classmethod
    def get_state(cls):
        now = timezone.now()
        if now < cls.start:
            return cls.BEFORE
        elif now < cls.end:
            return cls.DURING
        else:
            return cls.AFTER
        # return cls.objects.get().state


class Submission(models.Model):
    contact = models.ForeignKey(Contact, null=True)
    key = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    answers = models.CharField(max_length=65536, null=True, blank=True)
    key_sent = models.BooleanField(default=False)
    opened_link = models.BooleanField(default=False)
    marks = JSONField(default={})
    examiners = models.ManyToManyField(User, null=True, blank=True)
    end_time = models.CharField(max_length=5, null=True, blank=True)
    random_seed = models.IntegerField()

    def __unicode__(self):
        return ', '.join((self.last_name, self.first_name, self.email))

    @classmethod
    def generate_key(cls):
        key = ''
        while not key or key in [record['key'] for record in cls.objects.values('key')]:
            key = make_key(30)
        return key

    @classmethod
    def create(cls, first_name, last_name, email, key=None, contact=None):
        submission = cls(
            contact=contact,
            key=key if key else Submission.generate_key(),
            first_name=first_name,
            last_name=last_name,
            email=email,
            random_seed=random.randint(-2147483648, 2147483647)
        )

        submission.save()
        return submission

    def competition_link(self):
        return reverse('form_single', kwargs={'submission_id': self.id, 'key': self.key})

    def get_answers(self):
        return json.loads(self.answers) if self.answers else {}

    def shuffled_exercise_ids(self):
        exercise_ids = [e['id'] for e in exercises]
        seeded_random = random.Random(self.random_seed)
        seeded_random.shuffle(exercise_ids)
        return exercise_ids

    def current_exercise(self):
        answers = self.get_answers()
        for i, id in enumerate(self.shuffled_exercise_ids(), 1):
            if str(id) not in answers:
                return i, get_exercise_by_id(id)
        return None, None

    def get_mark(self, user_id, exercise_id):
        mark = None
        user_id = str(user_id)
        exercise_id = str(exercise_id)
        if self.marks and user_id in self.marks:
            mark = self.marks[user_id].get(exercise_id, None)
        return mark

    def set_mark(self, user_id, exercise_id, mark):
        user_id = str(user_id)
        exercise_id = str(exercise_id)
        if not self.marks:
            self.marks = dict()
        
        self.marks.setdefault(user_id, {})[exercise_id] = mark
        if mark == 'None':
            del self.marks[user_id][exercise_id]

    def get_exercise_marks_by_examiner(self, exercise_id):
        marks = dict()
        for examiner_id, examiner_marks in self.marks.items():
            mark = examiner_marks.get(exercise_id, None)
            if mark is not None:
                marks[examiner_id] = mark
        return marks

    def get_final_exercise_mark(self, exercise_id):
        exercise = get_exercise_by_id(exercise_id)
        if exercise_checked_manually(exercise):
            marks_by_examiner = self.get_exercise_marks_by_examiner(exercise_id)
            if len(marks_by_examiner):
                return sum(map(float, marks_by_examiner.values())) / float(len(marks_by_examiner))
            else:
                return None
        else:
            if not self.answers:
                return None
            answers = json.loads(self.answers)
            if exercise_id not in answers:
                return 0
            else:
                answer = answers[exercise_id]['closed_part']
                t = exercise['type']
                if t == 'edumed_uporzadkuj':
                    return exercise['points'] if map(int, answer) == exercise['answer'] else 0
                if t == 'edumed_przyporzadkuj':
                    toret = 0
                    for bucket_id, items in answer.items():
                        for item_id in items:
                            is_corect = False
                            if exercise.get('answer_mode', None) == 'possible_buckets_for_item':
                                is_correct = int(bucket_id) in exercise['answer'].get(item_id)
                            else:
                                is_correct = int(item_id) in exercise['answer'].get(bucket_id, [])
                            if is_correct:
                                toret += exercise['points_per_hit']
                    return toret
                if t == 'edumed_wybor':
                    if len(exercise['answer']) == 1:
                        if len(answer) and int(answer[0]) == exercise['answer'][0]:
                            return exercise['points']
                        else:
                            return 0
                    else:
                        toret = 0
                        if exercise.get('answer_mode', None) == 'all_or_nothing':
                            toret = exercise['points'] if map(int, answer) == exercise['answer'] else 0
                        else:
                            for answer_id in map(int, answer):
                                if answer_id in exercise['answer']:
                                    toret += exercise['points_per_hit']
                        return toret
                if t == 'edumed_prawdafalsz':
                    toret = 0
                    for idx, statement in enumerate(exercise['statements']):
                        if statement[1] == 'ignore':
                            continue
                        if answer[idx] == 'true':
                            given = True
                        elif answer[idx] == 'false':
                            given = False
                        else:
                            given = None
                        if given == statement[1]:
                            toret += exercise['points_per_hit']
                    return toret
                raise NotImplementedError

    @property
    def final_result(self):
        final = 0
        # for exercise_id in map(str,range(1, len(exercises) + 1)):
        for exercise_id in [str(x['id']) for x in exercises]:
            mark = self.get_final_exercise_mark(exercise_id)
            if mark is not None:
                final += mark
        return final

    @property
    def final_result_as_string(self):
        return ('%.2f' % self.final_result).rstrip('0').rstrip('.')


class Attachment(models.Model):
    submission = models.ForeignKey(Submission)
    exercise_id = models.IntegerField()
    tag = models.CharField(max_length=128, null=True, blank=True)
    file = models.FileField(upload_to='wtem/attachment')


class Assignment(models.Model):
    user = models.ForeignKey(User, unique=True)
    exercises = JSONField()

    def clean(self):
        if not isinstance(self.exercises, list):
            raise ValidationError(_('Assigned exercises must be declared in a list format'))
        # for exercise in self.exercises:
        #     if not isinstance(exercise, int) or exercise < 1:
        #         raise ValidationError(_('Invalid exercise id: %s' % exercise))

    def __unicode__(self):
        return self.user.username + ': ' + ','.join(map(str, self.exercises))


class Confirmation(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    contact = models.ForeignKey(Contact, null=True)
    key = models.CharField(max_length=30)
    confirmed = models.BooleanField(default=False)

    class Meta:
        ordering = ['contact__contact']

    @classmethod
    def create(cls, first_name, last_name, email, contact=None, key=None):
        confirmation = cls(
            contact=contact,
            key=key if key else make_key(30),
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        confirmation.save()
        return confirmation

    def absolute_url(self):
        return reverse('student_confirmation', args=(self.id, self.key))

    def readable_contact(self):
        return '%s <%s>' % (self.contact.body.get('przewodniczacy'), self.contact.contact)

    def school_phone(self):
        return '%s, tel. %s' % (self.contact.body.get('school'), self.contact.body.get('school_phone'))

    def age(self):
        return timezone.now() - self.contact.created_at

    def readable_age(self):
        td = self.age()
        return '%s dni, %s godzin' % (td.days, td.seconds/3600)

    def send_mail(self):
        mail_subject = render_to_string('contact/olimpiada/student_mail_subject.html').strip()
        mail_body = render_to_string(
            'contact/olimpiada/student_mail_body.html', {'confirmation': self})
        try:
            validate_email(self.email)
        except ValidationError:
            pass
        else:
            send_mail(mail_subject, mail_body, 'olimpiada@nowoczesnapolska.org.pl', [self.email],
                      fail_silently=True)


def exercise_checked_manually(exercise):
    return (exercise['type'] in ('open', 'file_upload')) or 'open_part' in exercise
