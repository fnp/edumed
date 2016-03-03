# -*- coding: utf-8 -*-
from haystack import indexes
from .models import Lesson


class LessonIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Lesson
