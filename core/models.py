# coding: utf-8

from django.db import models
import urllib2
from datetime import datetime, timedelta

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
        ordering = ('sigla',)

    def __unicode__(self):
        return self.sigla

    @staticmethod
    def obter_arquivo_csv(delta=0):
        if delta > 10:
            return ''
        try:
            now = datetime.now() - timedelta(days=delta)
            data = now.strftime('%Y%m%d')
            url = u'http://www4.bcb.gov.br/Download/fechamento/{0}.csv'.format(data)
            response = urllib2.urlopen(url)
            return response
        except urllib2.HTTPError, e:
            delta = delta + 1
            return Cotacao.obter_arquivo_csv(delta)

    @staticmethod
    def atualizar_cotacao_banco_central():
        response = Cotacao.obter_arquivo_csv()
        if response:
            csv = response.read()
            rows = csv.split('\n')
            for row in rows:
                cols = row.split(';')
                if len(cols) > 4:
                    try:
                        cotacao = Cotacao.objects.get(sigla=cols[3])
                    except Exception, e:
                        cotacao = Cotacao(sigla=cols[3])
                    cotacao.valor = float(cols[4].replace(',', '.'))
                    cotacao.save()


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

    def pais(self):
        return self.cidade.pais