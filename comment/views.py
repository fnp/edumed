from django.views.generic import ListView, DetailView
from django.conf import settings
from django.utils.translation import get_language

from django.core.urlresolvers import reverse

from .models import CommentDocument


class CommentDocumentList(ListView):
    model = CommentDocument

    def get_queryset(self, **kwargs):
        return super(CommentDocumentList, self).get_queryset(**kwargs).filter(language_code = get_language())

    def get_context_data(self, **kwargs):
        context = super(CommentDocumentList, self).get_context_data(**kwargs)
        context['form_href'] = reverse('contact_form', kwargs = dict(form_tag = 'mil'))
        return context


class CommentDocument(DetailView):
    model = CommentDocument

    def get_context_data(self, **kwargs):
        context = super(CommentDocument, self).get_context_data(**kwargs)
        context['comment_url'] = settings.COMMENT_URL
        return context