# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Senator.join_date'
        db.add_column(u'reps_senator', 'join_date',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Representative.join_date'
        db.add_column(u'reps_representative', 'join_date',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Senator.join_date'
        db.delete_column(u'reps_senator', 'join_date')

        # Deleting field 'Representative.join_date'
        db.delete_column(u'reps_representative', 'join_date')


    models = {
        u'reps.constituency': {
            'Meta': {'object_name': 'Constituency'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reps.State']"})
        },
        u'reps.district': {
            'Meta': {'object_name': 'District'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reps.State']"})
        },
        u'reps.lga': {
            'Meta': {'object_name': 'LGA'},
            'constituency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reps.Constituency']"}),
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reps.District']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reps.State']"})
        },
        u'reps.representative': {
            'Meta': {'object_name': 'Representative'},
            'constituency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reps.Constituency']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'join_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'reps.senator': {
            'Meta': {'object_name': 'Senator'},
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reps.District']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'join_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'reps.state': {
            'Meta': {'object_name': 'State'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['reps']