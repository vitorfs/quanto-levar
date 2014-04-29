# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Colaboracao.cidade'
        db.add_column(u'core_colaboracao', 'cidade',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Colaboracao.cidade'
        db.delete_column(u'core_colaboracao', 'cidade')


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
            'cidade': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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