# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.template.defaultfilters import filesizeformat

from stage2.models import Attachment, Mark


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['file']

    def __init__(self, assignment, file_no, label, extensions=None, *args, **kwargs):
        prefix = 'att%s-%s' % (assignment.id, file_no)
        super(AttachmentForm, self).__init__(*args, prefix=prefix, **kwargs)
        self.fields['file'].label = label
        if extensions:
            self.fields['file'].widget.attrs = {'data-ext': '|'.join(extensions)}
        self.extensions = extensions

    def clean_file(self):
        file = self.cleaned_data['file']
        if file.size > settings.MAX_UPLOAD_SIZE:
            raise forms.ValidationError(
                'Please keep filesize under %s. Current filesize: %s' % (
                    filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(file.size)))
        if self.extensions and ('.' not in file.name or file.name.rsplit('.', 1)[1].lower() not in self.extensions):
            raise forms.ValidationError('Incorrect extension, should be one of: %s' % ', '.join(self.extensions))
        return file


class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['points']
        widgets = {
            'points': forms.TextInput(attrs={'type': 'number', 'min': 0, 'step': '0.5'})
        }

    def __init__(self, answer, *args, **kwargs):
        super(MarkForm, self).__init__(*args, **kwargs)
        self.answer = answer
        self.fields['points'].widget.attrs['max'] = answer.assignment.max_points

    def clean_points(self):
        points = self.cleaned_data['points']
        if points > self.answer.assignment.max_points:
            raise forms.ValidationError('Too many points for this assignment')
        if points < 0:
            raise forms.ValidationError('Points cannot be negative')
        return points
