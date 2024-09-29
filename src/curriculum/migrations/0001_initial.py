# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Section'
        db.create_table('curriculum_section', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('curriculum', ['Section'])

        # Adding model 'Competence'
        db.create_table('curriculum_competence', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['curriculum.Section'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('curriculum', ['Competence'])

        # Adding model 'Level'
        db.create_table('curriculum_level', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('curriculum', ['Level'])

        # Adding model 'CompetenceLevel'
        db.create_table('curriculum_competencelevel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('competence', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['curriculum.Competence'])),
            ('level', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['curriculum.Level'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('curriculum', ['CompetenceLevel'])


    def backwards(self, orm):
        # Deleting model 'Section'
        db.delete_table('curriculum_section')

        # Deleting model 'Competence'
        db.delete_table('curriculum_competence')

        # Deleting model 'Level'
        db.delete_table('curriculum_level')

        # Deleting model 'CompetenceLevel'
        db.delete_table('curriculum_competencelevel')


    models = {
        'curriculum.competence': {
            'Meta': {'ordering': "['order']", 'object_name': 'Competence'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['curriculum.Section']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'curriculum.competencelevel': {
            'Meta': {'ordering': "['competence', 'level']", 'object_name': 'CompetenceLevel'},
            'competence': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['curriculum.Competence']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['curriculum.Level']"})
        },
        'curriculum.level': {
            'Meta': {'ordering': "['order']", 'object_name': 'Level'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'curriculum.section': {
            'Meta': {'ordering': "['order']", 'object_name': 'Section'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['curriculum']