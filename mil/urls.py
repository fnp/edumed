from django.conf.urls import patterns, include, url
from .views import root


urlpatterns = patterns('',
    url(r'^$', root, name="root"),
)
