from django.conf.urls import include, url

from fnpdjango.utils.urls import i18n_patterns
from .views import MILHomeView


urlpatterns = i18n_patterns('',
    url(r'^$', MILHomeView.as_view(), name="mil_home"),
    url(r'^kompetencje/', include('curriculum.urls')),
)

handler404 = 'edumed.views.mil_404_view'


