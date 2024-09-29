# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Curriculum'
        db.create_table('curriculum_curriculum', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['curriculum.CurriculumCourse'])),
            ('level', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['curriculum.CurriculumLevel'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=16)),
        ))
        db.send_create_signal('curriculum', ['Curriculum'])

        # Adding model 'CurriculumLevel'
        db.create_table('curriculum_curriculumlevel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=16, db_index=True)),
        ))
        db.send_create_signal('curriculum', ['CurriculumLevel'])

        # Adding model 'CurriculumCourse'
        db.create_table('curriculum_curriculumcourse', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
        ))
        db.send_create_signal('curriculum', ['CurriculumCourse'])


    def backwards(self, orm):
        # Deleting model 'Curriculum'
        db.delete_table('curriculum_curriculum')

        # Deleting model 'CurriculumLevel'
        db.delete_table('curriculum_curriculumlevel')

        # Deleting model 'CurriculumCourse'
        db.delete_table('curriculum_curriculumcourse')


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
        'curriculum.curriculum': {
            'Meta': {'object_name': 'Curriculum'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['curriculum.CurriculumCourse']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['curriculum.CurriculumLevel']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'curriculum.curriculumcourse': {
            'Meta': {'object_name': 'CurriculumCourse'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'curriculum.curriculumlevel': {
            'Meta': {'object_name': 'CurriculumLevel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '16', 'db_index': 'True'})
        },
        'curriculum.level': {
            'Meta': {'ordering': "['order']", 'object_name': 'Level'},
            'group': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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