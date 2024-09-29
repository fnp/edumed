# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from haystack.query import SearchQuerySet
from haystack.views import SearchView, search_view_factory
from haystack.forms import SearchForm
from pybb.models import Post

from .views import AddPostView, EditPostView


urlpatterns = patterns(
    '',
    url(r'^forum/(?P<forum_id>\d+)/topic/add/$', AddPostView.as_view()),
    url(r'^post/(?P<pk>\d+)/edit/$', EditPostView.as_view()),
)

PostsSearchQuerySet = SearchQuerySet().models(Post).highlight()

urlpatterns += patterns(
    'haystack.views',
    url(r'^szukaj/$', search_view_factory(
        view_class=SearchView,
        template='forum/search_results.html',
        searchqueryset=PostsSearchQuerySet,
        form_class=SearchForm
    ), name='forum_search'))
