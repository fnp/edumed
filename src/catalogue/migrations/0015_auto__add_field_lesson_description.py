# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Lesson.description'
        db.add_column(u'catalogue_lesson', 'description',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Lesson.description'
        db.delete_column(u'catalogue_lesson', 'description')


    models = {
        u'catalogue.attachment': {
            'Meta': {'ordering': "['slug', 'ext']", 'unique_together': "(['lesson', 'slug', 'ext'],)", 'object_name': 'Attachment'},
            'ext': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalogue.Lesson']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'catalogue.lesson': {
            'Meta': {'ordering': "['section', 'level', 'order']", 'object_name': 'Lesson'},
            'curriculum_courses': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['curriculum.CurriculumCourse']", 'symmetrical': 'False', 'blank': 'True'}),
            'dc': ('jsonfield.fields.JSONField', [], {'default': "'{}'"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'html_file': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['curriculum.Level']"}),
            'order': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'package': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'pdf': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalogue.Section']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'student_package': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'student_pdf': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'xml_file': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'catalogue.lessonstub': {
            'Meta': {'ordering': "['section', 'level', 'order']", 'object_name': 'LessonStub'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['curriculum.Level']"}),
            'order': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalogue.Section']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'})
        },
        u'catalogue.part': {
            'Meta': {'object_name': 'Part'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalogue.Lesson']"}),
            'pdf': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'student_pdf': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'catalogue.section': {
            'Meta': {'ordering': "['order']", 'object_name': 'Section'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'xml_file': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'curriculum.curriculumcourse': {
            'Meta': {'ordering': "['slug']", 'object_name': 'CurriculumCourse'},
            'accusative': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
        }
    }

    complete_apps = ['catalogue']