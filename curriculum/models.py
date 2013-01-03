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

class Competence(models.Model):
    section = models.ForeignKey(Section)
    name = models.CharField(_('name'), max_length=255)
    slug = models.SlugField(_('slug'))
    order = models.IntegerField(_('order'))

    class Meta:
        ordering = ['order']
        verbose_name = _('competence')
        verbose_name_plural = _('competences')

    def __unicode__(self):
        return self.name

class Level(models.Model):
    name = models.CharField(_('name'), max_length=255)
    slug = models.SlugField(_('slug'))
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
        return "%s/%s" % (self.competence, self.level)
