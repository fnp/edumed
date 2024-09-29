# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'CompetenceLevel.description'
        db.delete_column(u'curriculum_competencelevel', 'description')

        # Deleting field 'Section.name'
        db.delete_column(u'curriculum_section', 'name')

        # Deleting field 'Competence.name'
        db.delete_column(u'curriculum_competence', 'name')

        # Deleting field 'Level.group'
        db.delete_column(u'curriculum_level', 'group')

        # Deleting field 'Level.name'
        db.delete_column(u'curriculum_level', 'name')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'CompetenceLevel.description'
        raise RuntimeError("Cannot reverse this migration. 'CompetenceLevel.description' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Section.name'
        raise RuntimeError("Cannot reverse this migration. 'Section.name' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Competence.name'
        raise RuntimeError("Cannot reverse this migration. 'Competence.name' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Level.group'
        raise RuntimeError("Cannot reverse this migration. 'Level.group' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Level.name'
        raise RuntimeError("Cannot reverse this migration. 'Level.name' and its values cannot be restored.")

    models = {
        u'curriculum.competence': {
            'Meta': {'ordering': "['section', 'order']", 'object_name': 'Competence'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'name_pl': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['curriculum.Section']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'curriculum.competencelevel': {
            'Meta': {'ordering': "['competence', 'level']", 'object_name': 'CompetenceLevel'},
            'competence': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['curriculum.Competence']"}),
            'description_en': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'description_pl': ('django.db.models.fields.TextField', [], {'null': 'True'}),
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
            'group_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'group_pl': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'name_pl': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'curriculum.section': {
            'Meta': {'ordering': "['order']", 'object_name': 'Section'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'name_pl': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['curriculum']