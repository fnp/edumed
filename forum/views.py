from django.core.exceptions import ObjectDoesNotExist
import pybb.views
import pybb.forms

from catalogue.models import Lesson

from .forms import PostForm
from .models import Topic


class PostEditMixin(pybb.views.PostEditMixin):

    def get_form_class(self):
        toret = super(PostEditMixin, self).get_form_class()
        if issubclass(toret, pybb.forms.PostForm):
            toret = PostForm
        return toret

    def form_valid(self, form):
        toret = super(PostEditMixin, self).form_valid(form)

        pybb_post = self.object
        pybb_topic = pybb_post.topic
        topic, topic_created = Topic.objects.get_or_create(pybb_topic = pybb_topic)

        if pybb_post == pybb_topic.head:
            topic.lesson = form.cleaned_data['lesson']
            topic.save()

        return toret


class AddPostView(PostEditMixin, pybb.views.AddPostView):
    def get_context_data(self, **kwargs):
        ctx = super(AddPostView, self).get_context_data(**kwargs)
        ctx['lesson_editable'] = self._creates_new_topic()
        return ctx

    def _creates_new_topic(self):
        return self.forum is not None


class EditPostView(PostEditMixin, pybb.views.EditPostView):
    def get_context_data(self, **kwargs):
        ctx = super(EditPostView, self).get_context_data(**kwargs)
        ctx['lesson_editable'] = self._edits_topics_head()
        return ctx

    def _edits_topics_head(self):
        return self.object == self.object.topic.head

    def get_form_kwargs(self):
        kwargs = super(EditPostView, self).get_form_kwargs()
        try:
            lesson = self.object.topic.edumed_topic.lesson
        except ObjectDoesNotExist:
            lesson = None
        kwargs['initial']['lesson'] = lesson
        return kwargs
