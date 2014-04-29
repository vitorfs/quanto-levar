# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Cotacao'
        db.create_table(u'core_cotacao', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sigla', self.gf('django.db.models.fields.CharField')(unique=True, max_length=3)),
            ('valor', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'core', ['Cotacao'])

        # Adding model 'Pais'
        db.create_table(u'core_pais', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cotacao', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Cotacao'])),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('codigo', self.gf('django.db.models.fields.CharField')(unique=True, max_length=2)),
        ))
        db.send_create_signal(u'core', ['Pais'])

        # Adding model 'Cidade'
        db.create_table(u'core_cidade', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pais', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Pais'])),
            ('estado', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'core', ['Cidade'])

        # Adding model 'TipoDespesa'
        db.create_table(u'core_tipodespesa', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('categoria', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'core', ['TipoDespesa'])

        # Adding model 'Despesa'
        db.create_table(u'core_despesa', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cidade', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Cidade'])),
            ('tipo_despesa', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.TipoDespesa'])),
            ('nivel', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('valor', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'core', ['Despesa'])

        # Adding model 'Colaboracao'
        db.create_table(u'core_colaboracao', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descricao', self.gf('django.db.models.fields.TextField')(max_length=4000)),
        ))
        db.send_create_signal(u'core', ['Colaboracao'])


    def backwards(self, orm):
        # Deleting model 'Cotacao'
        db.delete_table(u'core_cotacao')

        # Deleting model 'Pais'
        db.delete_table(u'core_pais')

        # Deleting model 'Cidade'
        db.delete_table(u'core_cidade')

        # Deleting model 'TipoDespesa'
        db.delete_table(u'core_tipodespesa')

        # Deleting model 'Despesa'
        db.delete_table(u'core_despesa')

        # Deleting model 'Colaboracao'
        db.delete_table(u'core_colaboracao')


    models = {
        u'core.cidade': {
            'Meta': {'ordering': "('nome',)", 'object_name': 'Cidade'},
            'estado': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pais': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Pais']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'core.colaboracao': {
            'Meta': {'object_name': 'Colaboracao'},
            'descricao': ('django.db.models.fields.TextField', [], {'max_length': '4000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'core.cotacao': {
            'Meta': {'ordering': "('sigla',)", 'object_name': 'Cotacao'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sigla': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            'valor': ('django.db.models.fields.FloatField', [], {})
        },
        u'core.despesa': {
            'Meta': {'object_name': 'Despesa'},
            'cidade': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Cidade']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nivel': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'tipo_despesa': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.TipoDespesa']"}),
            'valor': ('django.db.models.fields.FloatField', [], {})
        },
        u'core.pais': {
            'Meta': {'ordering': "('nome',)", 'object_name': 'Pais'},
            'codigo': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'}),
            'cotacao': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Cotacao']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'core.tipodespesa': {
            'Meta': {'ordering': "('nome',)", 'object_name': 'TipoDespesa'},
            'categoria': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['core']