# -*- coding: utf-8 -*-
import json
import re

from django import forms

from .models import Submission, Attachment, exercises


class WTEMForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ('answers',)

    def __init__(self, *args, **kwargs):
        super(WTEMForm, self).__init__(*args, **kwargs)
        for exercise in exercises:
            if exercise['type'] == 'file_upload':
                self.fields['attachment_for_' + str(exercise['id'])] = forms.FileField(required=False)

    def save(self, commit=True):
        submission = super(WTEMForm, self).save(commit=commit)
        for name, attachment_file in self.files.items():
            m = re.match(r'attachment_for_(\d+)(?:__(.*))?', name)
            exercise_id = int(m.group(1))
            tag = m.group(2) or None
            try:
                attachment = Attachment.objects.get(submission=submission, exercise_id=exercise_id, tag=tag)
            except Attachment.DoesNotExist:
                attachment = Attachment(submission=submission, exercise_id=exercise_id, tag=tag)
            attachment.file = attachment_file
            attachment.save()


class WTEMSingleForm(forms.ModelForm):
    answers = forms.CharField()

    class Meta:
        model = Submission
        fields = []

    def __init__(self, *args, **kwargs):
        super(WTEMSingleForm, self).__init__(*args, **kwargs)
        i, exercise = self.instance.current_exercise()
        if exercise and exercise['type'] == 'file_upload':
            self.fields['attachment'] = forms.FileField(required=False)

    def save(self, commit=True):
        submission = self.instance
        answers = submission.get_answers()
        posted_answers = json.loads(self.cleaned_data['answers'])
        if type(posted_answers) != dict:
            raise ValueError('answers not dict')
        if len(posted_answers) != 1:
            raise ValueError('answers not single')
        exercise_id, answer = posted_answers.items()[0]
        # multipost
        if answers.get(exercise_id) == answer:
            return
        i, exercise = submission.current_exercise()
        if exercise_id != str(exercise['id']):
            raise ValueError('wrong exercise id')
        for answer in posted_answers.values():
            if not answer.get('closed_part', True):
                raise ValueError('no answer')
            answers[exercise_id] = answer
        submission.answers = json.dumps(answers)
        submission.save()
        for name, attachment_file in self.files.items():
            m = re.match(r'attachment(?:__(.*))?', name)
            tag = m.group(1) or None
            attachment, created = Attachment.objects.get_or_create(
                submission=submission, exercise_id=exercise_id, tag=tag)
            attachment.file = attachment_file
            attachment.save()
