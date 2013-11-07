# -*- coding: utf-8 -*-

import os

from django.contrib import admin
from django import forms
from django.utils import simplejson
from django.core.urlresolvers import reverse

from .models import Submission, Assignment
from .middleware import get_current_request


f = file(os.path.dirname(__file__) + '/fixtures/exercises.json')
exercises = simplejson.loads(f.read())
f.close()

def get_user_exercises(user):
    assignment = Assignment.objects.get(user = user)
    return [e for e in exercises if e['id'] in assignment.exercises]


readonly_fields = ('submitted_by', 'first_name', 'last_name', 'email', 'key', 'key_sent')


class SubmissionFormBase(forms.ModelForm):
    class Meta:
        model = Submission
        exclude = ('answers', 'marks', 'contact') + readonly_fields


def get_open_answer(answers, exercise):
    def get_option(options, id):
        for option in options:
            if option['id'] == int(id):
                return option

    exercise_id = str(exercise['id'])
    answer = answers[exercise_id]
    if exercise['type'] == 'open':
        toret = answer
    if exercise['type'] == 'edumed_wybor':
        ok = set(map(str, exercise['answer'])) == set(map(str,answer['closed_part']))
        toret = u'Czesc testowa [%s]:\n' % ('poprawna' if ok else 'niepoprawna')
        for selected in answer['closed_part']:
            option = get_option(exercise['options'], selected)
            toret += '%s: %s\n' % (selected, option['text'])
        toret += u'\nCzesc otwarta (%s):\n\n' % ' '.join(exercise['open_part'])
        toret += answer['open_part']

    return toret


def get_form(request, submission):
    fields = dict()
    if submission.answers:
        answers = simplejson.loads(submission.answers)
        user_exercises = get_user_exercises(request.user)
        for exercise in exercises:
            if exercise not in user_exercises:
                continue
            if exercise['type'] == 'open' or exercise.get('open_part', None):
                answer_field_name = 'exercise_%s' % exercise['id']
                mark_field_name = 'markof_%s_by_%s' % (exercise['id'], request.user.id)
                fields[answer_field_name] = forms.CharField(
                    widget = forms.Textarea(attrs={'readonly':True}),
                    initial = get_open_answer(answers, exercise),
                    label = 'Rozwiązanie zadania %s' % exercise['id']
                )

                fields[mark_field_name] = forms.ChoiceField(
                    choices = [(None, '-')] + [(i,i) for i in range(exercise['max_points']+1)],
                    initial = submission.get_mark(user_id = request.user.id, exercise_id = exercise['id']),
                    label = u'Twoja ocena zadania %s' % exercise['id']
                )
    return type('SubmissionForm', (SubmissionFormBase,), fields)


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'todo',)
    readonly_fields = readonly_fields

    def get_form(self, request, obj, **kwargs):
        return get_form(request, obj)
    
    def submitted_by(self, instance):
        if instance.contact:
            return '<a href="%s">%s</a>' % (
                reverse('admin:contact_contact_change', args = [instance.contact.id]),
                instance.contact.contact
            )
        return '-'
    submitted_by.allow_tags = True
    submitted_by.short_description = "Zgłoszony/a przez"

    def todo(self, submission):
        user = get_current_request().user
        user_exercises = get_user_exercises(user)
        user_marks = submission.marks.get(str(user.id), {})
        return ','.join([str(e['id']) for e in user_exercises if str(e['id']) not in user_marks.keys()])

    def save_model(self, request, submission, form, change):
        for name, value in form.cleaned_data.items():
            if name.startswith('markof_'):
                parts = name.split('_')
                exercise_id = parts[1]
                user_id = parts[3]
                submission.set_mark(user_id = user_id, exercise_id = exercise_id, mark = value)
        submission.save()


admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Assignment)