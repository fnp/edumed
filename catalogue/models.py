from django.db import models
from curriculum.models import Level

class Section(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    order = models.IntegerField()

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return self.title

class Lesson(models.Model):
    section = models.ForeignKey(Section)
    level = models.ForeignKey(Level)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    depth = models.IntegerField()
    order = models.IntegerField()

    xml_file = models.FileField(upload_to="catalogue/lesson/xml",
        null=True, blank=True) # FIXME: slug in paths
    package = models.FileField(upload_to="catalogue/lesson/package",
        null=True, blank=True)
    student_package = models.FileField(upload_to="catalogue/lesson/student",
        null=True, blank=True)
    html_file = models.FileField(upload_to="catalogue/lesson/html",
        null=True, blank=True)

    class Meta:
        ordering = ['section', 'level', 'depth', 'order']

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('catalogue_lesson', [self.slug])
