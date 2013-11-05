from django.conf.urls import patterns, url
from django.conf import settings
from .views import main, form, form_during

urlpatterns = patterns('',
    url(r'^$', main, name = 'wtem_main'),
    url(r'^_test/(?P<key>.*)/$', form_during),
    url(r'^(?P<key>.*)/$', form, name = 'wtem_form')
)
