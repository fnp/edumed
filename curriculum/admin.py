from django.contrib import admin
from .models import Competence, CompetenceLevel, Level, Section

class CompetenceLevelInline(admin.TabularInline):
    model = CompetenceLevel

class CompetenceAdmin(admin.ModelAdmin):
    model = Competence
    list_display = ['name', 'section', 'slug', 'order']
    inlines = [CompetenceLevelInline]

class LevelAdmin(admin.ModelAdmin):
    model = Level
    list_display = ['name', 'group', 'slug', 'order']

class SectionAdmin(admin.ModelAdmin):
    model = Section
    list_display = ['name', 'slug', 'order']


admin.site.register(Level, LevelAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Competence, CompetenceAdmin)
