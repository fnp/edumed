# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
    '',
    url(r'^potwierdzenie/(?P<id>.*)/(?P<key>.*)/$', views.confirmation, name='student_confirmation'),
    url(r'^_test/(?P<key>.*)/$', views.form_during),
    url(r'^(?P<submission_id>[^/]*)/(?P<key>[^/]*)/$', views.form, name='wtem_form'),
    url(r'^(?P<submission_id>[^/]*)/(?P<key>[^/]*)/start/$', views.start, name='wtem_start'),
)
