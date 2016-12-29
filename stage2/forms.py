# -*- coding: utf-8 -*-
from django import forms

from stage2.models import Attachment


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['file']

    def __init__(self, assignment, file_no, label, *args, **kwargs):
        prefix = 'att%s-%s' % (assignment.id, file_no)
        super(AttachmentForm, self).__init__(*args, prefix=prefix, **kwargs)
        self.fields['file'].label = label
