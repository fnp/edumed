from django.core.files import File
from django.core.urlresolvers import reverse
from django.db import models
from jsonfield import JSONField
from curriculum.models import Level


class Section(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    order = models.IntegerField()

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "%s#%s" % (reverse("catalogue_lessons"), self.slug)

    def syntetic_lesson(self):
        try:
            return self.lesson_set.filter(depth=0)[0]
        except IndexError:
            return None


class Lesson(models.Model):
    section = models.ForeignKey(Section)
    level = models.ForeignKey(Level)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    depth = models.IntegerField()
    order = models.IntegerField()
    dc = JSONField(default='{}')

    xml_file = models.FileField(upload_to="catalogue/lesson/xml",
        null=True, blank=True) # FIXME: slug in paths
    html_file = models.FileField(upload_to="catalogue/lesson/html",
        null=True, blank=True)
    package = models.FileField(upload_to="catalogue/lesson/pack",
        null=True, blank=True)
    student_package = models.FileField(upload_to="catalogue/lesson/student_pack",
        null=True, blank=True)
    pdf = models.FileField(upload_to="catalogue/lesson/pdf",
        null=True, blank=True)
    student_pdf = models.FileField(upload_to="catalogue/lesson/student_pdf",
        null=True, blank=True)

    class Meta:
        ordering = ['section', 'level', 'depth', 'order']

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('catalogue_lesson', [self.slug])

    @classmethod
    def publish(cls, infile):
        from librarian.parser import WLDocument
        from django.core.files.base import ContentFile
        # infile should be IOFile, now it's a regular file
        xml = infile.read()
        wldoc = WLDocument.from_string(xml)
        slug = wldoc.book_info.url.slug

        try:
            lesson = cls.objects.get(slug=slug)
        except cls.DoesNotExist:
            lesson = cls(slug=slug)

        # Save XML file
        lesson.xml_file.save('%s.xml' % slug, ContentFile(xml), save=False)
        lesson.title = wldoc.book_info.title
        #book.extra_info = wldoc.book_info.to_dict()

        # FIXME: 
        #lesson.level = Level.objects.get(slug=wldoc.book_info.audience)
        lesson.level = Level.objects.get(name=wldoc.book_info.audience)
        # TODO: no xml data?
        lesson.section = Section.objects.all()[0]
        lesson.order = 1
        lesson.depth = 1
        lesson.populate_dc()
        lesson.save()
        lesson.build_html()
        lesson.build_package()
        lesson.build_package(student=True)
        return lesson

    def populate_dc(self):
        from librarian.parser import WLDocument
        wldoc = WLDocument.from_file(self.xml_file.path)
        self.dc = wldoc.book_info.to_dict()
        self.save()

    def build_html(self):
        from librarian.parser import WLDocument
        wldoc = WLDocument.from_file(self.xml_file.path)
        html = wldoc.as_html()
        self.html_file.save("%s.html" % self.slug,
            File(open(html.get_filename())))

    def build_package(self, student=False):
        from StringIO import StringIO
        import zipfile
        from django.core.files.base import ContentFile
        buff = StringIO()
        zipf = zipfile.ZipFile(buff, 'w', zipfile.ZIP_STORED)
        zipf.write(self.xml_file.path, "pliki-zrodlowe/%s.xml" % self.slug)
        pdf = self.student_pdf if student else self.pdf
        if pdf:
            zipf.write(self.xml_file.path, 
                "%s%s.pdf" % (self.slug, "_student" if student else ""))
        zipf.close()
        fieldname = "student_package" if student else "package"
        getattr(self, fieldname).save(
            "%s%s.zip" % (self.slug, "_student" if student else ""),
            ContentFile(buff.getvalue()))


class Attachment(models.Model):
    lesson = models.ForeignKey(Lesson)
    file = models.FileField(upload_to="catalogue/attachment")


class Part(models.Model):
    lesson = models.ForeignKey(Lesson)
    pdf = models.FileField(upload_to="catalogue/part/pdf",
        null=True, blank=True)
    student_pdf = models.FileField(upload_to="catalogue/part/student_pdf",
        null=True, blank=True)
