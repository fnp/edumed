from django.conf.urls import include, url, patterns

from fnpdjango.utils.urls import i18n_patterns
from .views import mil_home_view


urlpatterns = i18n_patterns('',
    url(r'^$', mil_home_view, name="mil_home"),
    url(r'^kompetencje/', include('curriculum.urls')),
    url(r'^wez-udzial/', include('comment.urls')),
    url(r'^zglos/', include('contact.urls')),
)

handler404 = 'edumed.views.mil_404_view'


