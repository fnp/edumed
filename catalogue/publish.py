# -*- coding: utf-8
from django.core.files.base import ContentFile
from django.core.files import File
from librarian import DocProvider, IOFile
from librarian.pyhtml import EduModuleFormat
from librarian.pypdf import EduModulePDFFormat
from .models import Lesson, Attachment


class HtmlFormat(EduModuleFormat):
    def find_attachment(self, slug, fmt):
        lesson_slug = self.wldoc.book_info.url.slug
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
                return att
        else:
            return att

    def url_for_material(self, slug, fmt):
        return self.find_attachment(slug, fmt).file.url

    def url_for_image(self, slug, fmt, width=None):
        if width is None:
            return self.url_for_material(slug, fmt)

        lesson_slug = self.wldoc.book_info.url.slug
        th_slug = "thumb/%s__th%d" % (slug, width)
        try:
            # If already saved, use it.
            att = Attachment.objects.get(lesson__slug=lesson_slug,
                                         slug=th_slug, ext=fmt)
        except Attachment.DoesNotExist, e:
            from PIL import Image
            from StringIO import StringIO
            # Find full image, create thumbnail, save.
            src_att = self.find_attachment(slug, fmt)
            simg = Image.open(src_att.file.path)
            size = (width, simg.size[1]*width/simg.size[0])
            simg = simg.resize(size, Image.ANTIALIAS)

            tempfile = StringIO()
            img_format = "JPEG" if fmt.upper() == "JPG" else fmt
            simg.save(tempfile, format=img_format)
            att_name = "%s.%s" % (th_slug, fmt)
            lesson = Lesson.objects.get(slug=lesson_slug)
            att = lesson.attachment_set.create(slug=th_slug, ext=fmt)
            att.file.save(att_name, ContentFile(tempfile.getvalue()))
        return att.file.url

class PdfFormat(EduModulePDFFormat):
    pass


class OrmDocProvider(DocProvider):
    def by_slug(self, slug):
        """Should return a file-like object with a WL document XML."""
        return IOFile.from_filename(Lesson.objects.get(slug=slug).xml_file.path)
