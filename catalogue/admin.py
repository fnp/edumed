# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Attachment, Section, Lesson, LessonStub


class AttachmentInline(admin.TabularInline):
    model = Attachment


class LessonAdmin(admin.ModelAdmin):
    inlines = [AttachmentInline]
    list_display = ['title', 'section', 'type']
    list_filter = ['level', 'type']

admin.site.register(Section)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(LessonStub)
