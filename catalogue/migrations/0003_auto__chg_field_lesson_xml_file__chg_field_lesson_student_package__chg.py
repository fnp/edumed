# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Lesson.xml_file'
        db.alter_column('catalogue_lesson', 'xml_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True))

        # Changing field 'Lesson.student_package'
        db.alter_column('catalogue_lesson', 'student_package', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True))

        # Changing field 'Lesson.package'
        db.alter_column('catalogue_lesson', 'package', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True))

        # Changing field 'Lesson.html_file'
        db.alter_column('catalogue_lesson', 'html_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True))
        # Adding unique constraint on 'Section', fields ['title']
        db.create_unique('catalogue_section', ['title'])

        # Adding unique constraint on 'Section', fields ['slug']
        db.create_unique('catalogue_section', ['slug'])


    def backwards(self, orm):
        # Removing unique constraint on 'Section', fields ['slug']
        db.delete_unique('catalogue_section', ['slug'])

        # Removing unique constraint on 'Section', fields ['title']
        db.delete_unique('catalogue_section', ['title'])


        # User chose to not deal with backwards NULL issues for 'Lesson.xml_file'
        raise RuntimeError("Cannot reverse this migration. 'Lesson.xml_file' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Lesson.student_package'
        raise RuntimeError("Cannot reverse this migration. 'Lesson.student_package' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Lesson.package'
        raise RuntimeError("Cannot reverse this migration. 'Lesson.package' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Lesson.html_file'
        raise RuntimeError("Cannot reverse this migration. 'Lesson.html_file' and its values cannot be restored.")

    models = {
        'catalogue.lesson': {
            'Meta': {'ordering': "['section', 'level', 'depth', 'order']", 'object_name': 'Lesson'},
            'depth': ('django.db.models.fields.IntegerField', [], {}),
            'html_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['curriculum.Level']"}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'package': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.Section']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'student_package': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'xml_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'catalogue.section': {
            'Meta': {'object_name': 'Section'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'curriculum.level': {
            'Meta': {'ordering': "['order']", 'object_name': 'Level'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['catalogue']