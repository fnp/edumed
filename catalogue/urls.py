from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from .models import Section, Lesson
from .views import SectionView

urlpatterns = patterns('',
    url(r'^$',
        SectionView.as_view(),
        name="catalogue_lessons"),
    url(r'^(?P<slug>[^/]+)/$',
        DetailView.as_view(model=Lesson),
        name="catalogue_lesson"),
)
