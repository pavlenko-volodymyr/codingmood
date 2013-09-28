# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Commit.code_rate'
        db.alter_column(u'commits_commit', 'code_rate', self.gf('django.db.models.fields.FloatField')(default=0.0))

        # Changing field 'Commit.prev_date'
        db.alter_column(u'commits_commit', 'prev_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 9, 28, 0, 0)))

        # Changing field 'Commit.date'
        db.alter_column(u'commits_commit', 'date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 9, 28, 0, 0)))

    def backwards(self, orm):

        # Changing field 'Commit.code_rate'
        db.alter_column(u'commits_commit', 'code_rate', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'Commit.prev_date'
        db.alter_column(u'commits_commit', 'prev_date', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Commit.date'
        db.alter_column(u'commits_commit', 'date', self.gf('django.db.models.fields.DateTimeField')(null=True))

    models = {
        u'commits.commit': {
            'Meta': {'object_name': 'Commit'},
            'code_rate': ('django.db.models.fields.FloatField', [], {}),
            'commit_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'prev_date': ('django.db.models.fields.DateTimeField', [], {})
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