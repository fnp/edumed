# -*- coding: utf-8
from django.core.files import File
from django.core.urlresolvers import reverse
from librarian import DocProvider, IOFile
from librarian.pyhtml import EduModuleFormat
from librarian.pypdf import EduModulePDFFormat
from .models import Lesson, Attachment
from fnpdjango.utils.text.slughifi import slughifi


# TODO: Using sorl.thumbnail for now,
# but this should be done in Librarian,
# directly using convert or PIL as a fallback.
def get_image(src_img_path, width=None, default_width=1600, formats=('PNG', 'JPEG', 'GIF')):
    """ Returns an object with `url` and `storage` attributes,
        or None if using the original image is OK.
    """

    from PIL import Image
    from sorl.thumbnail import get_thumbnail

    # Does it need converting?
    # Yes, if width is given explicitly.
    convert = width is not None
    if not convert:
        # Looks like it doesn't need converting.
        # But let's try opening it and checking its type.
        try:
            simg = Image.open(src_img_path)
        except IOError:
            # It doesn't look like image,
            # but maybe it's convertable to one.
            convert = True
        else:
            if simg.format not in formats:
                # It's an image, but it's in some weird format.
                convert = True
                width = simg.size[0]

    if convert:
        if width is None:
            width = default_width
        try:
            return get_thumbnail(src_img_path, '%sx%s' % (width, 10*width))
        except:
            # hard to predict what solr raises on invalid image
            return None
    else:
        return None


class HtmlFormat(EduModuleFormat):
    IMAGE_FORMATS = ('PNG', 'JPEG', 'GIF')
    DEFAULT_IMAGE_WIDTH = 1600

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
        try:
            src_img = self.find_attachment(slug, fmt).file
        except self.MaterialNotFound:
            return ''
        img = get_image(src_img.path, width, self.DEFAULT_IMAGE_WIDTH, self.IMAGE_FORMATS)
        return (img or src_img).url

    def text_to_anchor(self, text):
        return slughifi(text)

    def get_forma_url(self, forma):
        return '%s#%s' % (
            reverse('catalogue_lesson', args=['metody']),
            self.text_to_anchor(forma)
        )

    def get_help_url(self, naglowek):
        return '%s%s#%s' % (
            '//edukacjamedialna.edu.pl',
            reverse('info', args=['jak-korzystac/']),
            self.naglowek_to_anchor(naglowek)
        )


class PdfFormat(EduModulePDFFormat):
    IMAGE_FORMATS = ('PNG', 'JPEG', 'GIF')
    DEFAULT_IMAGE_WIDTH = 1600

    def get_image(self, name):
        src_img = super(PdfFormat, self).get_image(name)
        img = get_image(
            src_img.get_filename(),
            default_width=self.DEFAULT_IMAGE_WIDTH,
            formats=self.IMAGE_FORMATS)
        if img:
            return IOFile.from_filename(img.storage.path(img))
        else:
            return src_img


class OrmDocProvider(DocProvider):
    def by_slug(self, slug):
        """Should return a file-like object with a WL document XML."""
        return IOFile.from_filename(Lesson.objects.get(slug=slug).xml_file.path)
