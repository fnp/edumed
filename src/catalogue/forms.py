# -*- coding: utf-8 -*-
import json
import os.path
import shutil
import urllib
from tempfile import mkdtemp

from django.forms import Form, CharField

from librarian import IOFile
from catalogue.models import Lesson


class LessonImportForm(Form):
    lesson_xml = CharField()
    gallery_url = CharField(required=False)
    attachments = CharField(required=False)

    def save(self):
        temp_dir = mkdtemp()
        attachment_names = json.loads(self.cleaned_data['attachments'])
        attachments = {}
        remote_gallery_url = self.cleaned_data['gallery_url']
        if remote_gallery_url and attachment_names:
            for attachment_name in attachment_names:
                attachment_url = ('%s%s' % (remote_gallery_url, attachment_name)).encode('utf-8')
                temp_filename = os.path.join(temp_dir, attachment_name)
                urllib.urlretrieve(attachment_url, temp_filename)
                attachments[attachment_name] = IOFile.from_filename(temp_filename)

        lesson = Lesson.publish(
            IOFile.from_string(self.cleaned_data['lesson_xml'], attachments=attachments))
        if os.path.isdir(temp_dir):
            shutil.rmtree(temp_dir)
        return lesson
