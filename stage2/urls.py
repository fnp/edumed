# -*- coding: utf-8 -*-
from django.conf.urls import url

from stage2 import views

urlpatterns = (
    url(r'^uczestnik/(?P<participant_id>[0-9]*)/(?P<key>.*)/$', views.participant_view, name='stage2_participant'),
    url(r'^upload/(?P<assignment_id>[0-9]*)/(?P<participant_id>[0-9]*)/(?P<key>.*)/$', views.upload,
        name='stage2_upload'),
    url(r'^plik/(?P<assignment_id>[0-9]*)/(?P<file_no>[0-9]*)/(?P<participant_id>[0-9]*)/(?P<key>.*)/$',
        views.get_file, name='stage2_participant_file'),
    url(r'^zadania/$', views.assignment_list, name='stage2_assignments'),
    url(r'^zadania/(?P<assignment_id>[0-9]*)/$', views.answer_list, name='stage2_answer_list'),
    url(r'^zadania/(?P<assignment_id>[0-9]*)/ocenione/$', views.marked_answer_list, name='stage2_marked_answers'),
    url(r'^plik/(?P<attachment_id>[0-9]*)/$', views.expert_download, name='stage2_expert_download'),
    url(r'^mark/(?P<answer_id>[0-9]*)/$', views.mark_answer, name='stage2_mark_answer'),
)
