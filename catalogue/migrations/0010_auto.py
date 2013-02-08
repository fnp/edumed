# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field curriculum_courses on 'Lesson'
        db.create_table('catalogue_lesson_curriculum_courses', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('lesson', models.ForeignKey(orm['catalogue.lesson'], null=False)),
            ('curriculumcourse', models.ForeignKey(orm['curriculum.curriculumcourse'], null=False))
        ))
        db.create_unique('catalogue_lesson_curriculum_courses', ['lesson_id', 'curriculumcourse_id'])


    def backwards(self, orm):
        # Removing M2M table for field curriculum_courses on 'Lesson'
        db.delete_table('catalogue_lesson_curriculum_courses')


    models = {
        'catalogue.attachment': {
            'Meta': {'ordering': "['slug', 'ext']", 'unique_together': "(['lesson', 'slug', 'ext'],)", 'object_name': 'Attachment'},
            'ext': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.Lesson']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'catalogue.lesson': {
            'Meta': {'ordering': "['section', 'level', 'order']", 'object_name': 'Lesson'},
            'curriculum_courses': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['curriculum.CurriculumCourse']", 'symmetrical': 'False'}),
            'dc': ('jsonfield.fields.JSONField', [], {'default': "'{}'"}),
            'html_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['curriculum.Level']"}),
            'order': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'package': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'pdf': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.Section']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'student_package': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'student_pdf': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'xml_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'catalogue.part': {
            'Meta': {'object_name': 'Part'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.Lesson']"}),
            'pdf': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'student_pdf': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'catalogue.section': {
            'Meta': {'ordering': "['order']", 'object_name': 'Section'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'xml_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'curriculum.curriculumcourse': {
            'Meta': {'object_name': 'CurriculumCourse'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'curriculum.level': {
            'Meta': {'ordering': "['order']", 'object_name': 'Level'},
            'group': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['catalogue']