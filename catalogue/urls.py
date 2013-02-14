from django.conf.urls import patterns, include, url
from .views import SectionView, LessonView

urlpatterns = patterns('',
    url(r'^$',
        SectionView.as_view(),
        name="catalogue_lessons"),
    url(r'^(?P<slug>[^/]+)/$',
        LessonView.as_view(),
        name="catalogue_lesson"),
)
