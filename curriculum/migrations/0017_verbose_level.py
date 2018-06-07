# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models


KLASA = ['I-III', 'IV-VI', 'VII-VIII', 'IV-VIII']
POZIOM = ['O', 'I', 'II', 'III', 'IV']
OTHER = {
    'LO': 'liceum i technikum',
}


class Migration(DataMigration):

    def forwards(self, orm):
        for level in orm.CurriculumLevel.objects.all():
            if level.title in KLASA:
                level.verbose = '%s klasa' % level.title
            elif level.title in POZIOM:
                level.verbose = '%s poziom edukacyjny' % level.title
            elif level.title in OTHER:
                level.verbose = OTHER[level.title]
            else:
                raise ValueError('Unknown level')
            level.save()

    def backwards(self, orm):
        pass

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
            'Meta': {'ordering': "['identifier']", 'object_name': 'Curriculum'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['curriculum.CurriculumCourse']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['curriculum.CurriculumLevel']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
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
            'title': ('django.db.models.fields.CharField', [], {'max_length': '16', 'db_index': 'True'}),
            'verbose': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'curriculum.level': {
            'Meta': {'ordering': "['order']", 'object_name': 'Level'},
            'group_en': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'group_pl': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'name_en': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'name_pl': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'package': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'student_package': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
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