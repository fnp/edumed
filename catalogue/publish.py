# -*- coding: utf-8
from django.core.files import File
from librarian import DocProvider, IOFile
from librarian.pyhtml import EduModuleFormat
from .models import Lesson, Attachment


class HtmlFormat(EduModuleFormat):
    def url_for_material(self, slug, fmt=None):
        lesson_slug = self.wldoc.book_info.url.slug
        if fmt is None:
            # We could try and find the file by slug here, but we won't.
            # User should supply the format explicitly anyway.
            fmt = self.DEFAULT_MATERIAL_FORMAT

        try:
            # If already saved, use it.
            att = Attachment.objects.get(lesson__slug=lesson_slug,
                                         slug=slug, ext=fmt)
        except Attachment.DoesNotExist, e:
            # If attached to source IOFile, save now.
            att_name = "%s.%s" % (slug, fmt)
            try:
                att_file = self.wldoc.source.attachments[att_name]
            except KeyError:
                print u"ATTACHMENT MISSING:", att_name
                raise self.MaterialNotFound()
            else:
                lesson = Lesson.objects.get(slug=lesson_slug)
                att = lesson.attachment_set.create(slug=slug, ext=fmt)
                att.file.save(att_name, File(att_file.get_file()))
                return att.file.url
        else:
            return att.file.url


class OrmDocProvider(DocProvider):
    def by_slug(self, slug):
        """Should return a file-like object with a WL document XML."""
        return IOFile.from_filename(Lesson.objects.get(slug=slug).xml_file.path)
