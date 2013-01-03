from django.conf.urls import patterns, include, url
from .views import CompetenceDetailView, CompetencesView

urlpatterns = patterns('',
    url(r'^$', CompetencesView.as_view(), name='curriculum'),
    url(r'^(?P<slug>[^/]+)/$', CompetenceDetailView.as_view(), name='curriculum_competence'),
)
