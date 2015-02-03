# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'State'
        db.create_table(u'reps_state', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'reps', ['State'])

        # Adding model 'Constituency'
        db.create_table(u'reps_constituency', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reps.State'])),
        ))
        db.send_create_signal(u'reps', ['Constituency'])

        # Adding model 'District'
        db.create_table(u'reps_district', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reps.State'])),
        ))
        db.send_create_signal(u'reps', ['District'])

        # Adding model 'LGA'
        db.create_table(u'reps_lga', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reps.State'])),
            ('constituency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reps.Constituency'])),
            ('district', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reps.District'])),
        ))
        db.send_create_signal(u'reps', ['LGA'])

        # Adding model 'Representative'
        db.create_table(u'reps_representative', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('constituency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reps.Constituency'])),
        ))
        db.send_create_signal(u'reps', ['Representative'])

        # Adding model 'Senator'
        db.create_table(u'reps_senator', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('district', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reps.District'])),
        ))
        db.send_create_signal(u'reps', ['Senator'])


    def backwards(self, orm):
        # Deleting model 'State'
        db.delete_table(u'reps_state')

        # Deleting model 'Constituency'
        db.delete_table(u'reps_constituency')

        # Deleting model 'District'
        db.delete_table(u'reps_district')

        # Deleting model 'LGA'
        db.delete_table(u'reps_lga')

        # Deleting model 'Representative'
        db.delete_table(u'reps_representative')

        # Deleting model 'Senator'
        db.delete_table(u'reps_senator')


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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'reps.senator': {
            'Meta': {'object_name': 'Senator'},
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reps.District']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'reps.state': {
            'Meta': {'object_name': 'State'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['reps']