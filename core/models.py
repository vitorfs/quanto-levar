# coding: utf-8

from django.db import models

class Nivel(models.Model):
    nome = models.CharField("Nome", max_length=255)

class Meta:
    verbose_name = 'Nivel'
    verbose_name_plural = 'Niveis'
    
class Categoria(models.Model):
    nome = models.CharField("Nome", max_length=255)

class Cotacao(models.Model):
    sigla = models.CharField(max_length=3, unique=True)
    valor = models.FloatField("Valor")
    
class Despesa(models.Model):
    categoria = models.ForeignKey(Categoria)
    nome = models.CharField("Nome", max_length=255)
    
class Pais(models.Model):
    cotacao = models.ForeignKey(Cotacao)
    nome = models.CharField("Nome", max_length=255)
    
class Cidade(models.Model):
    pais = models.ForeignKey(Pais)
    estado = models.CharField("Estado", max_length=255, null=True, blank=True)
    nome = models.CharField("Cidade", max_length=255)
    slug = models.SlugField(max_length=255)

class CidadeDespesa(models.Model):
    cidade = models.ForeignKey(Cidade)
    despesa = models.ForeignKey(Despesa)
    nivel = models.ForeignKey(Nivel)
    valor = models.FloatField("Valor")
    