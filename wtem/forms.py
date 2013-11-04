import os

from django import forms
from django.utils import simplejson

from .models import Submission, Attachment


class WTEMForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ('answers',)

    def __init__(self, *args, **kwargs):
        super(WTEMForm, self).__init__(*args, **kwargs)

        ## @@ move this one level up
        f = file(os.path.dirname(__file__) + '/fixtures/exercises.json')
        exercises = simplejson.loads(f.read())
        f.close()

        for exercise in exercises:
            if exercise['type'] != 'file_upload':
                continue
            self.fields['attachment_' + exercise['name']] = forms.FileField(required = False)

    def save(self):
        submission = super(WTEMForm, self).save()
        for file in self.files.values():
            attachment = Attachment(file = file, submission = submission)
            attachment.save()

