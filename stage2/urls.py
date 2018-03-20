# -*- coding: utf-8 -*-
from django.conf.urls import url

from stage2 import views

urlpatterns = (
    url(r'^uczestnik/(?P<participant_id>[0-9]*)/(?P<key>.*)/$', views.participant_view, name='stage2_participant'),
    url(r'^plik/(?P<assignment_id>[0-9]*)/(?P<file_no>[0-9]*)/(?P<participant_id>[0-9]*)/(?P<key>.*)/$',
        views.get_file, name='stage2_participant_file'),
    url(r'^zadania/$', views.assignment_list, name='stage2_assignments'),
    url(r'^zadania/(?P<assignment_id>[0-9]*)/$', views.answer_list, name='stage2_answer_list'),
    url(r'^zadania/(?P<assignment_id>[0-9]*)/ocenione/$', views.answer_list,
        kwargs={'marked': True}, name='stage2_marked_answers'),
    url(r'^plik/(?P<attachment_id>[0-9]*)/$', views.expert_download, name='stage2_expert_download'),
    url(r'^csv-results/', views.csv_results, name='stage2_csv_results'),
    url(r'^csv-details/(?P<assignment_id>[0-9]*)/$', views.csv_details, name='stage2_csv_details'),
)
