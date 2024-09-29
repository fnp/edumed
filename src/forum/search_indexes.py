# -*- coding: utf-8 -*-
from haystack import indexes
from pybb.models import Post


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Post
