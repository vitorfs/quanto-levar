from django.db import models

class Cotacao(models.Model):
    sigla = models.CharField(max_length=3, unique=True)
    valor = models.FloatField("Valor")

    class Meta:
      verbose_name = 'Cotacao'
      verbose_name_plural = 'Cotacaes'
    
class Despesa(models.Model):
    tipo = models.CharField("Tipo", max_length=255)

    class Meta:
      verbose_name = 'Despesa'
      verbose_name_plural = 'Despesas'
    
class Cidade(models.Model):
    cotacao = models.ForeignKey(Cotacao)
    cidade = models.CharField("Cidade", max_length=255)
    estado = models.CharField("Estado", max_length=255)
    pais = models.CharField("Pais", max_length=255)

    class Meta:
      verbose_name = 'Cidade'
      verbose_name_plural = 'Cidades'

class CidadeDespesa(models.Model):
    cidade = models.ForeignKey(Cidade)
    despesa = models.ForeignKey(Despesa)
    valor = models.FloatField("Valor")

    class Meta:
      verbose_name = 'Cidade'
      verbose_name_plural = 'Cidades'
    
    

