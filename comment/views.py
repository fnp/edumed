from django.views.generic import ListView, DetailView
from django.conf import settings

from .models import CommentDocument


class CommentDocumentList(ListView):
    model = CommentDocument


class CommentDocument(DetailView):
    model = CommentDocument

    def get_context_data(self, **kwargs):
        context = super(CommentDocument, self).get_context_data(**kwargs)
        context['comment_url'] = settings.COMMENT_URL
        return context