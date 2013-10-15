from django.conf.urls import patterns, include, url
from .views import MILHomeView


urlpatterns = patterns('',
    url(r'^$', MILHomeView.as_view(), name="mil_home"),
    url(r'^kompetencje/', include('curriculum.urls')),
)

handler404 = 'edumed.views.mil_404_view'


