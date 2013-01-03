# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Section'
        db.create_table('catalogue_section', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('catalogue', ['Section'])

        # Adding model 'Lesson'
        db.create_table('catalogue_lesson', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.Section'])),
            ('level', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['curriculum.Level'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('depth', self.gf('django.db.models.fields.IntegerField')()),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('xml_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('package', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('student_package', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('html_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('catalogue', ['Lesson'])


    def backwards(self, orm):
        # Deleting model 'Section'
        db.delete_table('catalogue_section')

        # Deleting model 'Lesson'
        db.delete_table('catalogue_lesson')


    models = {
        'catalogue.lesson': {
            'Meta': {'ordering': "['section', 'level', 'depth', 'order']", 'object_name': 'Lesson'},
            'depth': ('django.db.models.fields.IntegerField', [], {}),
            'html_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['curriculum.Level']"}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'package': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.Section']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'student_package': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'xml_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'catalogue.section': {
            'Meta': {'object_name': 'Section'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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