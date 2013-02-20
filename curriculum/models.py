# -*- coding: utf-8
import re
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Section(models.Model):
    name = models.CharField(_('name'), max_length=255)
    slug = models.SlugField(_('slug'))
    order = models.IntegerField(_('order'))

    class Meta:
        ordering = ['order']
        verbose_name = _('section')
        verbose_name_plural = _('sections')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "%s?s=%d" % (reverse("curriculum"), self.pk)

    def url_for_level(self, level):
        return "%s?s=%d&level=%s&d=1" % (reverse("curriculum"), self.pk, level.slug)
        

class Competence(models.Model):
    section = models.ForeignKey(Section)
    name = models.CharField(_('name'), max_length=255)
    slug = models.SlugField(_('slug'))
    order = models.IntegerField(_('order'))

    class Meta:
        ordering = ['section', 'order']
        verbose_name = _('competence')
        verbose_name_plural = _('competences')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "%s?c=%d" % (reverse("curriculum"), self.pk)

    def for_level(self, level):
        return self.competencelevel_set.get(level=level)

    def url_for_level(self, level):
        return self.for_level(level).get_absolute_url()

    @classmethod
    def from_text(cls, text):
        """Tries to return a Competence or a Section."""
        parts = re.split(ur'[-\u2013]', text, 1)
        if len(parts) == 1:
            return Section.objects.get(name__iexact=text.strip())
        else:
            return cls.objects.get(name__iexact=parts[1].strip())

class Level(models.Model):
    group = models.CharField(_('group'), max_length=255)
    name = models.CharField(_('name'), max_length=255)
    slug = models.CharField(_('slug'), max_length=255)
    order = models.IntegerField(_('order'))

    class Meta:
        ordering = ['order']
        verbose_name = _('educational level')
        verbose_name_plural = _('educational levels')

    def __unicode__(self):
        return self.name

class CompetenceLevel(models.Model):
    competence = models.ForeignKey(Competence)
    level = models.ForeignKey(Level)
    description = models.TextField(_('description'))

    class Meta:
        ordering = ['competence', 'level']
        verbose_name = _('competence on level')
        verbose_name_plural = _('competences on levels')

    def __unicode__(self):
        return u"%s/%s" % (self.competence, self.level)

    def get_absolute_url(self):
        return "%s?c=%d&level=%s&d=1" % (reverse("curriculum"), self.competence.pk, self.level.slug)



class CurriculumLevel(models.Model):
    title = models.CharField(max_length=16, db_index=True)

    class Meta:
        verbose_name = _("curriculum level")
        verbose_name_plural = _("curriculum levels")

    def __unicode__(self):
        return self.title


class CurriculumCourse(models.Model):
    title = models.CharField(max_length=255)
    accusative = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, db_index=True)

    class Meta:
        verbose_name = _("curriculum course")
        verbose_name_plural = _("curriculum courses")
        ordering = ['slug']

    def __unicode__(self):
        return self.title


class Curriculum(models.Model):
    """Official curriculum."""
    TYPES = {'c': u'Cele kształcenia', 't': u'Treści nauczania'}

    identifier = models.CharField(max_length=255, db_index=True)
    title = models.CharField(max_length=255)
    course = models.ForeignKey(CurriculumCourse)
    level = models.ForeignKey(CurriculumLevel)
    type = models.CharField(max_length=16, choices=TYPES.items())

    class Meta:
        verbose_name = _("curriculum item")
        verbose_name_plural = _("curriculum items")

    def __unicode__(self):
        return self.identifier

    @classmethod
    def from_text(cls, identifier, title):
        m = re.match(r"^\d+/(?P<level>[^/]+)/(?P<course>[^/]+)/"
                     "(?P<type>(?:%s))[^/]+(?P<roz>/roz)?" %
                        "|".join(cls.TYPES), identifier)
        assert m is not None, "Curriculum identifier doesn't match template."
        level, created = CurriculumLevel.objects.get_or_create(
                                       title=m.group('level'))
        def_title = m.group('course').title()
        course, created = CurriculumCourse.objects.get_or_create(
                                        slug=m.group('course').lower(),
                                        defaults={
                                            'title': def_title,
                                            'accusative': def_title,
                                        })
        type_ = m.group('type')
        if m.group('roz'):
            title += " (zakres rozszerzony)"

        try:
            curr = cls.objects.get(identifier=identifier)
        except cls.DoesNotExist:
            curr = cls(identifier=identifier)
        curr.title = title
        curr.course = course
        curr.level = level
        curr.type = type_
        curr.save()
        return curr

