import random
import string
import os

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import simplejson
from django.utils.translation import ugettext as _
from jsonfield import JSONField

from contact.models import Contact

f = file(os.path.dirname(__file__) + '/fixtures/exercises.json')
exercises = simplejson.loads(f.read())
f.close()

DEBUG_KEY = '12345'

class Submission(models.Model):
    contact = models.ForeignKey(Contact, null = True)
    key = models.CharField(max_length = 30, unique = True)
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    email = models.EmailField(max_length = 100, unique = True)
    answers = models.CharField(max_length = 65536, null = True, blank = True)
    key_sent = models.BooleanField(default = False)
    marks = JSONField()
    examiners = models.ManyToManyField(User, null = True, blank = True)

    def __unicode__(self):
        return ', '.join((self.last_name, self.first_name, self.email))

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
        exercise = exercises[int(exercise_id)-1]
        if exercise_checked_manually(exercise):
            marks_by_examiner = self.get_exercise_marks_by_examiner(exercise_id)
            if len(marks_by_examiner):
                return max(map(int, marks_by_examiner.values()))
            else:
                return None
        else:
            if not self.answers:
                return None
            answer = simplejson.loads(self.answers)[exercise_id]['closed_part']
            t = exercise['type']
            if t == 'edumed_uporzadkuj':
                return exercise['points'] if map(int, answer) == exercise['answer'] else 0
            if t == 'edumed_przyporzadkuj':
                toret = 0
                for bucket_id, items in answer.items():
                    for item_id in items:
                        if int(item_id) == exercise['answer'].get(bucket_id, None): # @@ We assume only one item per bucker for now...
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
                    for id in map(int, answer):
                        if id in exercise['answer']:
                            toret += exercise['points_per_hit']
                    return toret
            if t == 'edumed_prawdafalsz':
                toret = 0
                for idx, statement in enumerate(exercise['statements']):
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
        for exercise_id in map(str,range(1, len(exercises) + 1)):
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


def exercise_checked_manually(exercise):
    return (exercise['type'] in ('open', 'file_upload')) or 'open_part' in exercise