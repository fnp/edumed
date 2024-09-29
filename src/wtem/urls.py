# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from .views import form, form_during

urlpatterns = patterns(
    '',
    url(r'^_test/(?P<key>.*)/$', form_during),
    url(r'^(?P<key>.*)/$', form, name='wtem_form')
)
