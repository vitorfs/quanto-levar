# coding: utf-8

from django.db import models

class Nivel(models.Model):
    nome = models.CharField('Nome', max_length=255)

    class Meta:
        verbose_name = 'Nivel'
        verbose_name_plural = 'Níveis'
    
    def __unicode__(self):
        return self.nome


class Categoria(models.Model):
    nome = models.CharField('Nome', max_length=255)
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
    
    def __unicode__(self):
        return self.nome


class Cotacao(models.Model):
    sigla = models.CharField(max_length=3, unique=True)
    valor = models.FloatField('Valor')

    class Meta:
        verbose_name = 'Cotação'
        verbose_name_plural = 'Cotações'

    def __unicode__(self):
        return self.sigla


class Despesa(models.Model):
    categoria = models.ForeignKey(Categoria)
    nome = models.CharField('Nome', max_length=255)
    
    class Meta:
        verbose_name = 'Tipo de Despesa'
        verbose_name_plural = 'Tipos de Despesas'

    def __unicode__(self):
        return self.nome


class Pais(models.Model):
    cotacao = models.ForeignKey(Cotacao)
    nome = models.CharField('Nome', max_length=255)
    codigo = models.CharField('Código', max_length=2, unique=True)
    
    class Meta:
        verbose_name = 'País'
        verbose_name_plural = 'Países'

    def __unicode__(self):
        return self.nome


class Cidade(models.Model):
    pais = models.ForeignKey(Pais)
    estado = models.CharField('Estado', max_length=255, null=True, blank=True)
    nome = models.CharField('Cidade', max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'Cidade'
        verbose_name_plural = 'Cidades'

    def __unicode__(self):
        return self.nome


class CidadeDespesa(models.Model):
    cidade = models.ForeignKey(Cidade)
    despesa = models.ForeignKey(Despesa)
    nivel = models.ForeignKey(Nivel)
    valor = models.FloatField('Valor')
    
    class Meta:
        verbose_name = 'Despesa'
        verbose_name_plural = 'Despesas'
    
    def __unicode__(self):
        return u'{0} - {1}'.format(self.cidade.nome, self.despesa.nome)