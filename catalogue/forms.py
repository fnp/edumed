# -*- coding: utf-8 -*-
from django.forms import Form, FileField, CharField, ValidationError

from catalogue.models import Lesson


class LessonImportForm(Form):
    lesson_xml_file = FileField(required=False)
    lesson_xml = CharField(required=False)

    def clean(self):
        from django.core.files.base import ContentFile

        if not self.cleaned_data['lesson_xml_file']:
            if self.cleaned_data['lesson_xml']:
                self.cleaned_data['lesson_xml_file'] = \
                    ContentFile(self.cleaned_data['lesson_xml'].encode('utf-8'))
            else:
                raise ValidationError(u"Proszę dostarczyć XML.")
        return super(LessonImportForm, self).clean()

    def save(self, commit=True, **kwargs):
        return Lesson.publish(self.cleaned_data['book_xml_file'])
