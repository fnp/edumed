# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Lesson.type'
        db.add_column('catalogue_lesson', 'type',
                      self.gf('django.db.models.fields.CharField')(default='course', max_length=15, db_index=True),
                      keep_default=False)

        # Changing field 'Lesson.section'
        db.alter_column('catalogue_lesson', 'section_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.Section'], null=True))
        # Adding index on 'Lesson', fields ['order']
        db.create_index('catalogue_lesson', ['order'])

        if not db.dry_run:
            orm.Lesson.objects.filter(depth=0).update(type='synthetic')


    def backwards(self, orm):
        # Removing index on 'Lesson', fields ['order']
        db.delete_index('catalogue_lesson', ['order'])

        # Deleting field 'Lesson.type'
        db.delete_column('catalogue_lesson', 'type')

        section = 0
        if not db.dry_run:
            orm.Lesson.objects.filter(type='synthetic').update(depth=0)
            try:
                section = orm.Section.objects.all()[0]
            except orm.Section.DoesNotExist:
                pass

        # Changing field 'Lesson.section'
        db.alter_column('catalogue_lesson', 'section_id',
            self.gf('django.db.models.fields.related.ForeignKey')(default=section, to=orm['catalogue.Section']))


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
            'dc': ('jsonfield.fields.JSONField', [], {'default': "'{}'"}),
            'depth': ('django.db.models.fields.IntegerField', [], {}),
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
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
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
