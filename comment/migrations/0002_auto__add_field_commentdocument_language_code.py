# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'CommentDocument.language_code'
        db.add_column(u'comment_commentdocument', 'language_code',
                      self.gf('django.db.models.fields.CharField')(default='pl', max_length=2),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'CommentDocument.language_code'
        db.delete_column(u'comment_commentdocument', 'language_code')


    models = {
        u'comment.commentdocument': {
            'Meta': {'ordering': "['order']", 'object_name': 'CommentDocument'},
            'comment_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'default': "'pl'", 'max_length': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['comment']