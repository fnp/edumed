from django.contrib import admin

from .models import CommentDocument


class CommentDocumentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(CommentDocument, CommentDocumentAdmin)
