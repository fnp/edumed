# -*- coding: utf-8 -*-
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
            if exercise['type'] != 'file_upload':
                continue
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
