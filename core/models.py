# coding: utf-8

from django.db import models
import urllib2
from datetime import datetime, timedelta

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


class Pais(models.Model):
    cotacao = models.ForeignKey(Cotacao)
    nome = models.CharField('Nome', max_length=255)
    codigo = models.CharField('Código', max_length=2, unique=True)
    
    class Meta:
        verbose_name = 'País'
        verbose_name_plural = 'Países'
        ordering = ('nome',)

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
        ordering = ('nome',)

    def __unicode__(self):
        return self.nome

    def _listar_despesas(self, categoria):
        '''
            Método privado para retornar apenas tipos de despesas cadastradas para a cidade
        '''
        despesas = Despesa.objects.filter(cidade=self, tipo_despesa__categoria=categoria)
        tipos_despesas = []
        for despesa in despesas:
            tipos_despesas.append(despesa.tipo_despesa)
        return set(tipos_despesas)

    def listar_alimentacao(self):
        return self._listar_despesas(TipoDespesa.ALIMENTACAO)

    def listar_transporte(self):
        return self._listar_despesas(TipoDespesa.TRANSPORTE)

    def listar_hospedagem(self):
        return self._listar_despesas(TipoDespesa.HOSPEDAGEM)

    def listar_niveis_alimentacao(self):
        despesas = Despesa.objects.filter(cidade=self).exclude(nivel__isnull=True)
        niveis = {}
        for despesa in despesas:
            niveis[despesa.nivel] = despesa.get_nivel_display()
        return niveis


class TipoDespesa(models.Model):
    ALIMENTACAO = 'A'
    TRANSPORTE = 'T'
    HOSPEDAGEM = 'H'

    CATEGORIAS = (
        (ALIMENTACAO, u'Alimentação'),
        (TRANSPORTE, u'Transporte'),
        (HOSPEDAGEM, u'Hospedagem'),
        )

    categoria = models.CharField(max_length=1, choices=CATEGORIAS)
    nome = models.CharField('Nome', max_length=255)
    
    class Meta:
        verbose_name = 'Tipo de Despesa'
        verbose_name_plural = 'Tipos de Despesas'
        ordering = ('nome',)

    def __unicode__(self):
        return self.nome


class Despesa(models.Model):
    ECONOMICO = 'E'
    MODERADO = 'M'
    CARO = 'C'

    NIVEIS = (
        (ECONOMICO, u'Econômico'),
        (MODERADO, u'Moderado'),
        (CARO, u'Caro'),
        )

    cidade = models.ForeignKey(Cidade)
    tipo_despesa = models.ForeignKey(TipoDespesa)
    nivel = models.CharField(max_length=1, choices=NIVEIS, blank=True, null=True)
    valor = models.FloatField('Valor')
    
    class Meta:
        verbose_name = 'Despesa'
        verbose_name_plural = 'Despesas'
    
    def __unicode__(self):
        return self.tipo_despesa.nome

    def pais(self):
        return self.cidade.pais