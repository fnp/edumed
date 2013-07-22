from django.core.files import File
from django.core.urlresolvers import reverse
from django.db import models
from jsonfield import JSONField
from curriculum.models import Level, Curriculum, CurriculumCourse


class Section(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    order = models.IntegerField()
    xml_file = models.FileField(upload_to="catalogue/section/xml",
        null=True, blank=True, max_length=255)

    class Meta:
        ordering = ['order']

    class IncompleteError(BaseException):
        pass

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "%s#%s" % (reverse("catalogue_lessons"), self.slug)

    @classmethod
    def publish(cls, infile):
        from librarian.parser import WLDocument
        from django.core.files.base import ContentFile
        xml = infile.get_string()
        wldoc = WLDocument.from_string(xml)

        try:
            lessons = [Lesson.objects.get(slug=part.slug)
                        for part in wldoc.book_info.parts]
        except Lesson.DoesNotExist, e:
            raise cls.IncompleteError(part.slug)

        slug = wldoc.book_info.url.slug
        try:
            section = cls.objects.get(slug=slug)
        except cls.DoesNotExist:
            section = cls(slug=slug, order=0)

        # Save XML file
        section.xml_file.save('%s.xml' % slug, ContentFile(xml), save=False)
        section.title = wldoc.book_info.title
        section.save()

        section.lesson_set.all().update(section=None)
        for i, lesson in enumerate(lessons):
            lesson.section = section
            lesson.order = i
            lesson.save()

        return section

    def syntetic_lesson(self, level):
        try:
            return self.lesson_set.filter(type='synthetic', level=level)[0]
        except IndexError:
            return None


class Lesson(models.Model):
    section = models.ForeignKey(Section, null=True, blank=True)
    level = models.ForeignKey(Level)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    type = models.CharField(max_length=15, db_index=True)
    order = models.IntegerField(db_index=True)
    dc = JSONField(default='{}')
    curriculum_courses = models.ManyToManyField(CurriculumCourse, blank=True)

    xml_file = models.FileField(upload_to="catalogue/lesson/xml",
        null=True, blank=True, max_length=255)
    html_file = models.FileField(upload_to="catalogue/lesson/html",
        null=True, blank=True, max_length=255)
    package = models.FileField(upload_to="catalogue/lesson/pack",
        null=True, blank=True, max_length=255)
    student_package = models.FileField(upload_to="catalogue/lesson/student_pack",
        null=True, blank=True, max_length=255)
    pdf = models.FileField(upload_to="catalogue/lesson/pdf",
        null=True, blank=True, max_length=255)
    student_pdf = models.FileField(upload_to="catalogue/lesson/student_pdf",
        null=True, blank=True, max_length=255)

    class Meta:
        ordering = ['section', 'level', 'order']

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('catalogue_lesson', [self.slug])

    @classmethod
    def publish(cls, infile):
        from librarian.parser import WLDocument
        from django.core.files.base import ContentFile
        xml = infile.get_string()
        wldoc = WLDocument.from_string(xml)

        # Check if not section metadata block.
        if wldoc.book_info.parts:
            return Section.publish(infile)
        
        slug = wldoc.book_info.url.slug
        try:
            lesson = cls.objects.get(slug=slug)
            lesson.attachment_set.all().delete()
        except cls.DoesNotExist:
            lesson = cls(slug=slug, order=0)

        # Save XML file
        lesson.xml_file.save('%s.xml' % slug, ContentFile(xml), save=False)
        lesson.title = wldoc.book_info.title

        lesson.level = Level.objects.get(slug=wldoc.book_info.audience)
        lesson.populate_dc()
        lesson.build_html(infile=infile)
        lesson.build_pdf(infile=infile)
        lesson.build_pdf(student=True, infile=infile)
        lesson.build_package()
        lesson.build_package(student=True)
        return lesson

    def populate_dc(self):
        from librarian.parser import WLDocument
        wldoc = WLDocument.from_file(self.xml_file.path)
        self.dc = wldoc.book_info.to_dict()
        self.type = self.dc["type"]
        self.save()

        courses = set()
        for identifier in wldoc.book_info.curriculum:
            try:
                curr = Curriculum.objects.get(identifier=identifier)
            except Curriculum.DoesNotExist:
                pass
            else:
                courses.add(curr.course)
        self.curriculum_courses = courses

    def wldocument(self, infile=None):
        from librarian import IOFile
        from librarian.parser import WLDocument
        from .publish import OrmDocProvider

        if infile is None:
            infile = IOFile.from_filename(self.xml_file.path)
            for att in self.attachment_set.all():
                infile.attachments["%s.%s" % (att.slug, att.ext)] = \
                    IOFile.from_filename(att.file.path)
        return WLDocument(infile, provider=OrmDocProvider())

    def build_html(self, infile=None):
        from .publish import HtmlFormat
        wldoc = self.wldocument(infile)
        html = HtmlFormat(wldoc).build()
        self.html_file.save("%s.html" % self.slug,
            File(open(html.get_filename())))

    def build_pdf(self, student=False, infile=None):
        from .publish import PdfFormat
        wldoc = self.wldocument(infile)
        if student:
            pdf = PdfFormat(wldoc).build()
            self.student_pdf.save("%s.pdf" % self.slug,
                File(open(pdf.get_filename())))
        else:
            pdf = PdfFormat(wldoc, teacher=True).build()
            self.pdf.save("%s.pdf" % self.slug,
                File(open(pdf.get_filename())))

    def add_to_zip(self, zipf, student=False, prefix=''):
        zipf.write(self.xml_file.path,
            "%spliki-zrodlowe/%s.xml" % (prefix, self.slug))
        pdf = self.student_pdf if student else self.pdf
        if pdf:
            zipf.write(pdf.path, 
                "%s%s%s.pdf" % (prefix, self.slug, "_student" if student else ""))
        for attachment in self.attachment_set.all():
            zipf.write(attachment.file.path,
                u"%smaterialy/%s.%s" % (prefix, attachment.slug, attachment.ext))
            
        

    def build_package(self, student=False):
        from StringIO import StringIO
        import zipfile
        from django.core.files.base import ContentFile
        buff = StringIO()
        zipf = zipfile.ZipFile(buff, 'w', zipfile.ZIP_STORED)
        self.add_to_zip(zipf, student)
        zipf.close()
        fieldname = "student_package" if student else "package"
        getattr(self, fieldname).save(
            "%s%s.zip" % (self.slug, "_student" if student else ""),
            ContentFile(buff.getvalue()))

    def get_syntetic(self):
        if self.section is None: return None
        return self.section.syntetic_lesson(self.level)

    def get_other_level(self):
        if self.section is None: return None
        other_levels = self.section.lesson_set.exclude(level=self.level)
        if other_levels.exists():
            return other_levels[0].level

    def get_previous(self):
        if self.section is None: return None
        try:
            return self.section.lesson_set.filter(
                type=self.type, level=self.level,
                order__lt=self.order).order_by('-order')[0]
        except IndexError:
            return None

    def get_next(self):
        if self.section is None: return None
        try:
            return self.section.lesson_set.filter(
                type=self.type, level=self.level,
                order__gt=self.order).order_by('order')[0]
        except IndexError:
            return None


class Attachment(models.Model):
    slug = models.CharField(max_length=255)
    ext = models.CharField(max_length=15)
    lesson = models.ForeignKey(Lesson)
    file = models.FileField(upload_to="catalogue/attachment")

    class Meta:
        ordering = ['slug', 'ext']
        unique_together = ['lesson', 'slug', 'ext']

    def __unicode__(self):
        return "%s.%s" % (self.slug, self.ext)


class Part(models.Model):
    lesson = models.ForeignKey(Lesson)
    pdf = models.FileField(upload_to="catalogue/part/pdf",
        null=True, blank=True)
    student_pdf = models.FileField(upload_to="catalogue/part/student_pdf",
        null=True, blank=True)


class LessonStub(models.Model):
    section = models.ForeignKey(Section, null=True, blank=True)
    level = models.ForeignKey(Level)
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=15, db_index=True)
    order = models.IntegerField(db_index=True)

    class Meta:
        ordering = ['section', 'level', 'order']

    def __unicode__(self):
        return self.title
