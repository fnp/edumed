# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from stage2 import views

urlpatterns = (
    url(r'^uczestnik/(?P<participant_id>[0-9]*)/(?P<key>.*)/$', views.participant_view, name='stage2_participant'),
    url(r'^upload/(?P<assignment_id>[0-9]*)/(?P<participant_id>[0-9]*)/(?P<key>.*)/$', views.upload,
        name='stage2_upload'),
    url(r'^plik/(?P<assignment_id>[0-9]*)/(?P<file_no>[0-9]*)/(?P<participant_id>[0-9]*)/(?P<key>.*)/$',
        views.get_file, name='stage2_participant_file')
)
