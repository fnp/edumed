from django.db import models
from django.core.urlresolvers import reverse


class CommentDocument(models.Model):
    name = models.CharField(max_length = 255, unique = True)
    slug = models.SlugField(max_length = 255, unique = True)
    comment_id = models.CharField(max_length = 255, unique = True)
    order = models.IntegerField()

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('comment_document', kwargs = dict(slug = self.slug))
