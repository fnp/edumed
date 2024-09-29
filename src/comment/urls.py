# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import CommentDocumentList, CommentDocument


urlpatterns = patterns(
    '',
    url('^$', CommentDocumentList.as_view(), name='comment_document_index'),
    url('^(?P<slug>[^/]+)/$', CommentDocument.as_view(), name='comment_document')
)
