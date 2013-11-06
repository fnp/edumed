# -*- coding: utf-8 -*-

import os

from django.contrib import admin
from django import forms
from django.utils import simplejson
from django.core.urlresolvers import reverse

from .models import Submission, Assignment


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


def get_form(request, submission):
    fields = dict()
    if submission.answers:
        answers = simplejson.loads(submission.answers)
        user_exercises = get_user_exercises(request.user)
        for exercise in exercises:
            if exercise not in user_exercises:
                continue
            if exercise['type'] == 'open':
                answer_field_name = 'exercise_%s' % exercise['id']
                mark_field_name = 'markof_%s_by_%s' % (exercise['id'], request.user.id)
                fields[answer_field_name] = forms.CharField(
                    widget = forms.Textarea(attrs={'readonly':True}),
                    initial = answers[str(exercise['id'])],
                    label = 'Rozwiązanie zadania %s' % exercise['id']
                )

                fields[mark_field_name] = forms.ChoiceField(
                    choices = [(None, '-')] + [(i,i) for i in range(exercise['max_points']+1)],
                    initial = submission.get_mark(user_id = request.user.id, exercise_id = exercise['id']),
                    label = u'Twoja ocena zadania %s' % exercise['id']
                )
    return type('SubmissionForm', (SubmissionFormBase,), fields)


class SubmissionAdmin(admin.ModelAdmin):
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