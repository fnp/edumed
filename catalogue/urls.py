from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from .models import Section, Lesson

urlpatterns = patterns('',
    url(r'^$',
        ListView.as_view(model=Section),
        name="catalogue_lessons"),
    url(r'^(?P<slug>[^/]+)/$',
        DetailView.as_view(model=Lesson),
        name="catalogue_lesson"),
)
