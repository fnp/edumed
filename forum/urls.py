from django.conf.urls import patterns, include, url

from .views import AddPostView, EditPostView


urlpatterns = patterns('',
    url(r'^forum/(?P<forum_id>\d+)/topic/add/$', AddPostView.as_view()),
    url(r'^post/(?P<pk>\d+)/edit/$', EditPostView.as_view()),
)