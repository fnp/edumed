# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Participant'
        db.create_table(u'stage2_participant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contact.Contact'], null=True)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=100)),
            ('key_sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'stage2', ['Participant'])

        # Adding model 'Assignment'
        db.create_table(u'stage2_assignment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('deadline', self.gf('django.db.models.fields.DateTimeField')()),
            ('max_points', self.gf('django.db.models.fields.IntegerField')()),
            ('file_descriptions', self.gf('jsonfield.fields.JSONField')()),
        ))
        db.send_create_signal(u'stage2', ['Assignment'])

        # Adding model 'Answer'
        db.create_table(u'stage2_answer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stage2.Participant'])),
            ('assignment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stage2.Assignment'])),
            ('uploaded_files', self.gf('jsonfield.fields.JSONField')()),
        ))
        db.send_create_signal(u'stage2', ['Answer'])

        # Adding unique constraint on 'Answer', fields ['participant', 'assignment']
        db.create_unique(u'stage2_answer', ['participant_id', 'assignment_id'])

        # Adding model 'Mark'
        db.create_table(u'stage2_mark', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('expert', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('answer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stage2.Answer'])),
            ('points', self.gf('django.db.models.fields.DecimalField')(max_digits=3, decimal_places=1)),
        ))
        db.send_create_signal(u'stage2', ['Mark'])

        # Adding unique constraint on 'Mark', fields ['expert', 'answer']
        db.create_unique(u'stage2_mark', ['expert_id', 'answer_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Mark', fields ['expert', 'answer']
        db.delete_unique(u'stage2_mark', ['expert_id', 'answer_id'])

        # Removing unique constraint on 'Answer', fields ['participant', 'assignment']
        db.delete_unique(u'stage2_answer', ['participant_id', 'assignment_id'])

        # Deleting model 'Participant'
        db.delete_table(u'stage2_participant')

        # Deleting model 'Assignment'
        db.delete_table(u'stage2_assignment')

        # Deleting model 'Answer'
        db.delete_table(u'stage2_answer')

        # Deleting model 'Mark'
        db.delete_table(u'stage2_mark')


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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stage2.Participant']"}),
            'uploaded_files': ('jsonfield.fields.JSONField', [], {})
        },
        u'stage2.assignment': {
            'Meta': {'ordering': "['deadline']", 'object_name': 'Assignment'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'deadline': ('django.db.models.fields.DateTimeField', [], {}),
            'file_descriptions': ('jsonfield.fields.JSONField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_points': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'stage2.mark': {
            'Meta': {'unique_together': "(['expert', 'answer'],)", 'object_name': 'Mark'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stage2.Answer']"}),
            'expert': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'points': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '1'})
        },
        u'stage2.participant': {
            'Meta': {'object_name': 'Participant'},
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