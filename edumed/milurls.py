from django.conf.urls import include, url, patterns

from fnpdjango.utils.urls import i18n_patterns
from .views import MILHomeView


urlpatterns = i18n_patterns('',
    url(r'^kompetencje/', include('curriculum.urls')),
    url(r'^wez-udzial/', include('comment.urls'))
)

urlpatterns += patterns('',
    url(r'^$', 'django.contrib.flatpages.views.flatpage', {'url': '/'}, name="mil_home_pl"),
    url(r'^en/$', 'django.contrib.flatpages.views.flatpage', {'url': '/en/'}, name="mil_home_en")
)

handler404 = 'edumed.views.mil_404_view'


