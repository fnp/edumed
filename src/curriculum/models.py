# -*- coding: utf-8
import re
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _, get_language
from fnpdjango.storage import BofhFileSystemStorage
from fnpdjango.utils.models.translation import add_translatable
from fnpdjango.utils.text.slughifi import slughifi as slugify

bofh_storage = BofhFileSystemStorage()


class Section(models.Model):
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

add_translatable(Section, {
    'name': models.CharField(_('name'), max_length=255, default='')
})


class Competence(models.Model):
    section = models.ForeignKey(Section)
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
        lookup_field_name = 'name_%s__iexact' % get_language()
        if len(parts) == 1:
            return Section.objects.get(**{lookup_field_name: text.strip()})
        else:
            return cls.objects.get(**{lookup_field_name: parts[1].strip()})

add_translatable(Competence, {
    'name': models.CharField(_('name'), max_length=255, default='')
})


class Level(models.Model):
    slug = models.CharField(_('slug'), max_length=255, unique=True)
    meta_name = models.CharField(_('meta name'), max_length=255, unique=True)
    order = models.IntegerField(_('order'))
    package = models.FileField(
        upload_to=lambda i, f: "curriculum/pack/edukacjamedialna_%s.zip" % i.slug,
        null=True, blank=True, max_length=255, storage=bofh_storage)
    student_package = models.FileField(
        upload_to=lambda i, f: "curriculum/pack/edukacjamedialna_%s_uczen.zip" % i.slug,
        null=True, blank=True, max_length=255, storage=bofh_storage)

    class Meta:
        ordering = ['order']
        verbose_name = _('educational level')
        verbose_name_plural = _('educational levels')

    def __unicode__(self):
        return self.name

    def length_course(self):
        return self.lesson_set.filter(type='course').count()

    def length_synthetic(self):
        return self.lesson_set.filter(type='synthetic').count()

    def build_package(self, student):
        from StringIO import StringIO
        import zipfile
        from django.core.files.base import ContentFile
        from catalogue.templatetags.catalogue_tags import level_box
        from catalogue.models import Lesson

        buff = StringIO()
        zipf = zipfile.ZipFile(buff, 'w', zipfile.ZIP_STORED)

        lessons = level_box(self)['lessons']
        for i, lesson in enumerate(lessons['synthetic']):
            prefix = 'Skrocony kurs/%d %s/' % (i, lesson.slug)
            lesson.add_to_zip(zipf, student, prefix)
        for c, (section, clessons) in enumerate(lessons['course'].items()):
            assert section, clessons
            for i, lesson in enumerate(clessons):
                prefix = 'Pelny kurs/%d %s/%d %s/' % (c, section.slug, i, lesson.slug)
                lesson.add_to_zip(zipf, student, prefix)
        for i, lesson in enumerate(lessons['project']):
            prefix = 'Projekty/%d %s/' % (i, lesson.slug)
            lesson.add_to_zip(zipf, student, prefix)
        # Add all appendix lessons, from all levels.
        for lesson in Lesson.objects.filter(type='appendix'):
            # ugly fix
            if self.slug in ('przedszkole', 'sp1-3', 'sp4-6'):
                if lesson.slug == 'slowniczek':
                    continue
            else:
                if lesson.slug == 'slowniczek-sp':
                    continue
            prefix = '%s/' % lesson.slug
            lesson.add_to_zip(zipf, student, prefix)
        zipf.close()

        fieldname = "student_package" if student else "package"
        getattr(self, fieldname).save(None, ContentFile(buff.getvalue()))

    def build_packages(self):
        self.build_package(False)
        self.build_package(True)


add_translatable(Level, {
    'name': models.CharField(_('name'), max_length=255, default=''),
    'group': models.CharField(_('group'), max_length=255, default='')
})


class CompetenceLevel(models.Model):
    competence = models.ForeignKey(Competence)
    level = models.ForeignKey(Level)

    class Meta:
        ordering = ['competence', 'level']
        verbose_name = _('competence on level')
        verbose_name_plural = _('competences on levels')

    def __unicode__(self):
        return u"%s/%s" % (self.competence, self.level)

    def get_absolute_url(self):
        return "%s?c=%d&level=%s&d=1" % (reverse("curriculum"), self.competence.pk, self.level.slug)

add_translatable(CompetenceLevel, {
    'description': models.TextField(_('description'), default='')
})


class CurriculumLevel(models.Model):
    title = models.CharField(max_length=16, db_index=True)
    verbose = models.CharField(max_length=32)

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
    TYPES = {'c': u'Cele kształcenia', 't': u'Treści nauczania', 'o': u'Osiągnięcia'}

    identifier = models.CharField(max_length=255, db_index=True, unique=True)
    title = models.CharField(max_length=1024)
    course = models.ForeignKey(CurriculumCourse)
    level = models.ForeignKey(CurriculumLevel)
    type = models.CharField(max_length=16, choices=TYPES.items())

    class Meta:
        ordering = ['identifier']
        verbose_name = _("curriculum item")
        verbose_name_plural = _("curriculum items")

    def __unicode__(self):
        return self.identifier

    @classmethod
    def from_text(cls, identifier, title):
        m = re.match(r"^\d+/(?P<level>[^/]+)/(?P<course>[^/]+)/"
                     r"(?P<type>(?:%s))[^/]+(?P<roz>/roz)?" % "|".join(cls.TYPES), identifier)
        assert m is not None, "Curriculum identifier doesn't match template."
        level, created = CurriculumLevel.objects.get_or_create(
                                       title=m.group('level'))
        if created:
            print 'created level:', m.group('level')
        def_title = m.group('course').capitalize()
        course, created = CurriculumCourse.objects.get_or_create(
                                        slug=slugify(m.group('course')),
                                        defaults={
                                            'title': def_title,
                                            'accusative': def_title,
                                        })
        if created:
            print 'created course:', slugify(m.group('course')), def_title
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
