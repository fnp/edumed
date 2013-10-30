from django.conf.urls import patterns, url
from .views import main

urlpatterns = patterns('',
    url(r'^$', main, name = 'wtem_main')
)