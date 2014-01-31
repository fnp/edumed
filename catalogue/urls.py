from django.conf.urls import patterns, include, url
from .views import LessonListView, LessonView

urlpatterns = patterns('',
    url(r'^$',
        LessonListView.as_view(),
        name="catalogue_lessons"),
    url(r'^(?P<slug>[^/]+)/$',
        LessonView.as_view(),
        name="catalogue_lesson"),
)
