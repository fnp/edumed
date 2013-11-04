# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Submission'
        db.create_table(u'wtem_submission', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contact.Contact'], null=True)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=100)),
            ('answers', self.gf('django.db.models.fields.CharField')(max_length=65536, null=True, blank=True)),
        ))
        db.send_create_signal(u'wtem', ['Submission'])

        # Adding model 'Attachment'
        db.create_table(u'wtem_attachment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('submission', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wtem.Submission'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'wtem', ['Attachment'])


    def backwards(self, orm):
        # Deleting model 'Submission'
        db.delete_table(u'wtem_submission')

        # Deleting model 'Attachment'
        db.delete_table(u'wtem_attachment')


    models = {
        u'contact.contact': {
            'Meta': {'ordering': "('-created_at',)", 'object_name': 'Contact'},
            'body': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'form_tag': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'})
        },
        u'wtem.attachment': {
            'Meta': {'object_name': 'Attachment'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'submission': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wtem.Submission']"})
        },
        u'wtem.submission': {
            'Meta': {'object_name': 'Submission'},
            'answers': ('django.db.models.fields.CharField', [], {'max_length': '65536', 'null': 'True', 'blank': 'True'}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contact.Contact']", 'null': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '100'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['wtem']