# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'CompetenceLevel.description_en'
        db.alter_column(u'curriculum_competencelevel', 'description_en', self.gf('django.db.models.fields.TextField')())

        # Changing field 'CompetenceLevel.description_pl'
        db.alter_column(u'curriculum_competencelevel', 'description_pl', self.gf('django.db.models.fields.TextField')())

        # Changing field 'Section.name_en'
        db.alter_column(u'curriculum_section', 'name_en', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Section.name_pl'
        db.alter_column(u'curriculum_section', 'name_pl', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Competence.name_pl'
        db.alter_column(u'curriculum_competence', 'name_pl', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Competence.name_en'
        db.alter_column(u'curriculum_competence', 'name_en', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Level.name_pl'
        db.alter_column(u'curriculum_level', 'name_pl', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Level.group_pl'
        db.alter_column(u'curriculum_level', 'group_pl', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Level.group_en'
        db.alter_column(u'curriculum_level', 'group_en', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Level.name_en'
        db.alter_column(u'curriculum_level', 'name_en', self.gf('django.db.models.fields.CharField')(max_length=255))

    def backwards(self, orm):

        # Changing field 'CompetenceLevel.description_en'
        db.alter_column(u'curriculum_competencelevel', 'description_en', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'CompetenceLevel.description_pl'
        db.alter_column(u'curriculum_competencelevel', 'description_pl', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Section.name_en'
        db.alter_column(u'curriculum_section', 'name_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Section.name_pl'
        db.alter_column(u'curriculum_section', 'name_pl', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Competence.name_pl'
        db.alter_column(u'curriculum_competence', 'name_pl', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Competence.name_en'
        db.alter_column(u'curriculum_competence', 'name_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Level.name_pl'
        db.alter_column(u'curriculum_level', 'name_pl', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Level.group_pl'
        db.alter_column(u'curriculum_level', 'group_pl', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Level.group_en'
        db.alter_column(u'curriculum_level', 'group_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Level.name_en'
        db.alter_column(u'curriculum_level', 'name_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

    models = {
        u'curriculum.competence': {
            'Meta': {'ordering': "['section', 'order']", 'object_name': 'Competence'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'name_pl': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['curriculum.Section']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'curriculum.competencelevel': {
            'Meta': {'ordering': "['competence', 'level']", 'object_name': 'CompetenceLevel'},
            'competence': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['curriculum.Competence']"}),
            'description_en': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'description_pl': ('django.db.models.fields.TextField', [], {'default': "''"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['curriculum.Level']"})
        },
        u'curriculum.curriculum': {
            'Meta': {'object_name': 'Curriculum'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['curriculum.CurriculumCourse']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['curriculum.CurriculumLevel']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        u'curriculum.curriculumcourse': {
            'Meta': {'ordering': "['slug']", 'object_name': 'CurriculumCourse'},
            'accusative': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'curriculum.curriculumlevel': {
            'Meta': {'object_name': 'CurriculumLevel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '16', 'db_index': 'True'})
        },
        u'curriculum.level': {
            'Meta': {'ordering': "['order']", 'object_name': 'Level'},
            'group_en': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'group_pl': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'name_pl': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'curriculum.section': {
            'Meta': {'ordering': "['order']", 'object_name': 'Section'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'name_pl': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['curriculum']