# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
    'contact.views',
    url(r'^(?P<form_tag>[^/]+)/$', views.form, name='contact_form'),
    url(r'^(?P<form_tag>[^/]+)/edit/(?P<contact_id>[0-9]+)/(?P<key>[0-9a-zA-Z]+)/$', views.form, name='edit_form'),
    url(r'^(?P<form_tag>[^/]+)/thanks/$', views.thanks, name='contact_thanks'),
    url(r'^attachment/(?P<contact_id>\d+)/(?P<tag>[^/]+)/$', views.attachment, name='contact_attachment'),
    url(r'^attachment/(?P<contact_id>\d+)/(?P<tag>[^/]+)/(?P<key>[0-9a-zA-Z]+)/$', views.attachment_key,
        name='contact_attachment_key'),
    url(r'^results/(?P<contact_id>\d+)/(?P<digest>[0-9a-f]+)/', views.results, name='contact_results'),
)
