from django.contrib import admin
from .models import (Competence, CompetenceLevel, Level, Section,
    CurriculumCourse, CurriculumLevel, Curriculum)

class CompetenceLevelInline(admin.TabularInline):
    model = CompetenceLevel

class CompetenceAdmin(admin.ModelAdmin):
    model = Competence
    list_display = ['name_pl', 'name_en', 'section', 'slug', 'order']
    inlines = [CompetenceLevelInline]

class LevelAdmin(admin.ModelAdmin):
    model = Level
    list_display = ['name_pl', 'name_en', 'group_pl', 'group_en', 'slug', 'order']

class SectionAdmin(admin.ModelAdmin):
    model = Section
    list_display = ['name_pl', 'name_en', 'slug', 'order']


admin.site.register(Level, LevelAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Competence, CompetenceAdmin)

admin.site.register(CurriculumCourse)
admin.site.register(CurriculumLevel)
admin.site.register(Curriculum)
