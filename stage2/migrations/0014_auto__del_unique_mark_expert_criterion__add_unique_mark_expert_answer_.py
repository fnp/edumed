# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Mark', fields ['expert', 'criterion']
        db.delete_unique(u'stage2_mark', ['expert_id', 'criterion_id'])

        # Adding unique constraint on 'Mark', fields ['expert', 'answer', 'criterion']
        db.create_unique(u'stage2_mark', ['expert_id', 'answer_id', 'criterion_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Mark', fields ['expert', 'answer', 'criterion']
        db.delete_unique(u'stage2_mark', ['expert_id', 'answer_id', 'criterion_id'])

        # Adding unique constraint on 'Mark', fields ['expert', 'criterion']
        db.create_unique(u'stage2_mark', ['expert_id', 'criterion_id'])


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contact.contact': {
            'Meta': {'ordering': "('-created_at',)", 'object_name': 'Contact'},
            'body': ('jsonfield.fields.JSONField', [], {}),
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'form_tag': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'stage2.answer': {
            'Meta': {'unique_together': "(['participant', 'assignment'],)", 'object_name': 'Answer'},
            'assignment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stage2.Assignment']"}),
            'complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'experts': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'stage2_assigned_answers'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'field_values': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'need_arbiter': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stage2.Participant']"})
        },
        u'stage2.assignment': {
            'Meta': {'ordering': "['deadline', 'title']", 'object_name': 'Assignment'},
            'arbiters': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'stage2_arbitrated'", 'blank': 'True', 'to': u"orm['auth.User']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'content_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'deadline': ('django.db.models.fields.DateTimeField', [], {}),
            'experts': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'stage2_assignments'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'field_descriptions': ('jsonfield.fields.JSONField', [], {'default': '[]', 'blank': 'True'}),
            'file_descriptions': ('jsonfield.fields.JSONField', [], {'default': '[]', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_points': ('django.db.models.fields.IntegerField', [], {}),
            'supervisors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'stage2_supervised'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'stage2.attachment': {
            'Meta': {'ordering': "['file_no']", 'object_name': 'Attachment'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stage2.Answer']"}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'file_no': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'stage2.fieldoption': {
            'Meta': {'ordering': "['set', 'value']", 'object_name': 'FieldOption'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stage2.Answer']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'set': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stage2.FieldOptionSet']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'stage2.fieldoptionset': {
            'Meta': {'object_name': 'FieldOptionSet'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'})
        },
        u'stage2.mark': {
            'Meta': {'unique_together': "(['expert', 'answer', 'criterion'],)", 'object_name': 'Mark'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stage2.Answer']"}),
            'criterion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stage2.MarkCriterion']"}),
            'expert': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'points': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '1'})
        },
        u'stage2.markcriterion': {
            'Meta': {'ordering': "['order']", 'unique_together': "(['assignment', 'order'],)", 'object_name': 'MarkCriterion'},
            'assignment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stage2.Assignment']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'max_points': ('django.db.models.fields.IntegerField', [], {}),
            'order': ('django.db.models.fields.IntegerField', [], {})
        },
        u'stage2.participant': {
            'Meta': {'object_name': 'Participant'},
            'complete_set': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contact.Contact']", 'null': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '100'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'key_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['stage2']