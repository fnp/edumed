from django.contrib import admin
from .models import Attachment, Section, Lesson

class AttachmentInline(admin.TabularInline):
    model = Attachment

class LessonAdmin(admin.ModelAdmin):
    inlines = [AttachmentInline]

admin.site.register(Section)
admin.site.register(Lesson, LessonAdmin)
