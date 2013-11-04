from django.conf.urls import patterns, url
from django.conf import settings
from .views import main, form

urlpatterns = patterns('',
    url(r'^$', main, name = 'wtem_main'),
    url(r'^(?P<key>.*)/$', form, name = 'wtem_form')
)
