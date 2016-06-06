# -*- coding: utf-8 -*-
from django.forms import Form, CharField

from librarian import IOFile
from catalogue.models import Lesson


class LessonImportForm(Form):
    lesson_xml = CharField()

    def save(self, commit=True, **kwargs):
        return Lesson.publish(IOFile.from_string(self.cleaned_data['lesson_xml']))
