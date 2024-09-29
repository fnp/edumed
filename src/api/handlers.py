# -*- coding: utf-8 -*-
import json

from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.utils.functional import lazy
from piston.handler import BaseHandler
from piston.utils import rc

from catalogue.forms import LessonImportForm
from catalogue.models import Lesson

API_BASE = EDUMED_BASE = MEDIA_BASE = lazy(
    lambda: u'https://' + Site.objects.get_current().domain, unicode)()


class LessonDetails(object):
    """Custom fields used for representing Lessons."""

    @classmethod
    def href(cls, lesson):
        """ Returns an URI for a Lesson in the API. """
        return API_BASE + reverse("api_lesson", args=[lesson.slug])

    @classmethod
    def url(cls, lesson):
        """ Returns Lesson's URL on the site. """
        return EDUMED_BASE + lesson.get_absolute_url()


class LessonDetailHandler(BaseHandler, LessonDetails):
    """ Main handler for Lesson objects.

    Responsible for single Lesson details.
    """
    allowed_methods = ['GET']
    fields = ['title', 'url']

    def read(self, request, lesson):
        """ Returns details of a lesson, identified by a slug. """
        try:
            return Lesson.objects.get(slug=lesson)
        except Lesson.DoesNotExist:
            return rc.NOT_FOUND


class LessonsHandler(LessonDetailHandler):
    allowed_methods = ('GET', 'POST')
    model = Lesson
    fields = ['href', 'title', 'url']

    def create(self, request, *args, **kwargs):
        if not request.user.has_perm('catalogue.add_lesson'):
            return rc.FORBIDDEN

        data = json.loads(request.POST.get('data'))
        form = LessonImportForm(data)
        if form.is_valid():
            form.save()
            return rc.CREATED
        else:
            return rc.NOT_FOUND
