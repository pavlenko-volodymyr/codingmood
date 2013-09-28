# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Commit.commit_id'
        db.alter_column(u'commits_commit', 'commit_id', self.gf('django.db.models.fields.CharField')(default='', max_length=100))

    def backwards(self, orm):

        # Changing field 'Commit.commit_id'
        db.alter_column(u'commits_commit', 'commit_id', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

    models = {
        u'commits.commit': {
            'Meta': {'object_name': 'Commit'},
            'code_rate': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'commit_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'prev_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'commits.repository': {
            'Meta': {'object_name': 'Repository'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['commits']