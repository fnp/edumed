# -*- coding: utf-8 -*-

import os

from django.contrib import admin
from django import forms
from django.utils import simplejson
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

from .models import Submission, Assignment, Attachment, exercises
from .middleware import get_current_request


def get_user_exercises(user):
    try:
        assignment = Assignment.objects.get(user = user)
        return [e for e in exercises if e['id'] in assignment.exercises]
    except Assignment.DoesNotExist:
        return []


readonly_fields = ('submitted_by', 'first_name', 'last_name', 'email', 'key', 'key_sent')

class AttachmentWidget(forms.Widget):
    def render(self, name, value, *args, **kwargs):
        if value:
            a_tag = '<a href="%s">%s</a>' % (value, value)
        else:
            a_tag = 'brak'
        return mark_safe(('<input type="hidden" name="%s" value="%s"/>' + a_tag) % (name, value))

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
        if isinstance(answer, list):
            toret = ''
            for part in answer:
                field = get_option(exercise['fields'], part['id'])
                toret += '- %s:\n\n%s\n\n' % (field['caption'], part['text'])
        else:
            toret = answer
    if exercise['type'] == 'edumed_wybor':
        ok = set(map(str, exercise['answer'])) == set(map(str,answer['closed_part']))
        toret = u'Czesc testowa [%s]:\n' % ('poprawna' if ok else 'niepoprawna')
        for selected in answer['closed_part']:
            option = get_option(exercise['options'], selected)
            toret += '%s: %s\n' % (selected, option['text'])
        else:
            toret += u'<nie wybrano odpowiedzi>\n'
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
            
            answer_field_name = 'exercise_%s' % exercise['id']
            mark_field_name = 'markof_%s_by_%s' % (exercise['id'], request.user.id)
            if exercise['type'] in ('open', 'file_upload') or exercise.get('open_part', None):
                if exercise['type'] == 'file_upload':
                    try:
                        attachment = Attachment.objects.get(submission = submission, exercise_id = exercise['id'])
                    except Attachment.DoesNotExist:
                        attachment = None
                    widget = AttachmentWidget
                    initial = attachment.file.url if attachment else None
                else:
                    widget = forms.Textarea(attrs={'readonly':True})
                    initial = get_open_answer(answers, exercise)

                fields[answer_field_name] = forms.CharField(
                        widget = widget,
                        initial = initial,
                        label = 'Rozwiązanie zadania %s' % exercise['id']
                )

                fields[mark_field_name] = forms.ChoiceField(
                    choices = [(None, '-')] + [(i,i) for i in range(exercise['max_points']+1)],
                    initial = submission.get_mark(user_id = request.user.id, exercise_id = exercise['id']),
                    label = u'Twoja ocena zadania %s' % exercise['id']
                )

    if not request.user.is_superuser:
        class Meta(SubmissionFormBase.Meta):
            pass
        Meta.exclude += ('examiners',)
        fields['Meta'] = Meta

    return type('SubmissionForm', (SubmissionFormBase,), fields)


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'todo', 'examiners_repr')
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

    def examiners_repr(self, submission):
        return ', '.join([u.username for u in submission.examiners.all()])
    examiners_repr.short_description = 'Przypisani'

    def save_model(self, request, submission, form, change):
        for name, value in form.cleaned_data.items():
            if name.startswith('markof_'):
                parts = name.split('_')
                exercise_id = parts[1]
                user_id = parts[3]
                submission.set_mark(user_id = user_id, exercise_id = exercise_id, mark = value)
        submission.save()

    def changelist_view(self, request, extra_context=None):
        context = dict(examiners = [])
        assignments = Assignment.objects.all()
        if not request.user.is_superuser:
            assignments = assignments.filter(user = request.user)
        for assignment in assignments:
            examiner = dict(name = assignment.user.username, todo = 0)
            for submission in Submission.objects.filter(examiners = assignment.user):
                for exercise_id in assignment.exercises:
                    if submission.get_mark(user_id = assignment.user.id, exercise_id = exercise_id) is None:
                        examiner['todo'] += 1
            context['examiners'].append(examiner)
        return super(SubmissionAdmin, self).changelist_view(request, extra_context = context)

    def queryset(self, request):
        qs = super(SubmissionAdmin, self).queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(examiners = request.user)
        return qs


admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Assignment)