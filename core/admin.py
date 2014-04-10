from django.contrib import admin
from core.models import *

class NivelAdmin(admin.ModelAdmin):
  list_display = ('id', 'nome')
  
class CategoriaAdmin(admin.ModelAdmin):
  list_display = ('id', 'nome')

class CotacaoAdmin(admin.ModelAdmin):
  list_display = ('id', 'sigla', 'valor')
  
class DespesaAdmin(admin.ModelAdmin):
  list_display = ('id', 'categoria', 'nome')
  
class PaisAdmin(admin.ModelAdmin):
  list_display = ('id', 'cotacao', 'nome')
  
class CidadeAdmin(admin.ModelAdmin):
  list_display = ('id', 'pais', 'estado', 'nome')
  
class CidadeDespesaAdmin(admin.ModelAdmin):
  list_display = ('id', 'cidade', 'despesa', 'nivel', 'valor')

admin.site.register(Nivel, NivelAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Cotacao, CotacaoAdmin)
admin.site.register(Despesa, DespesaAdmin)
admin.site.register(Pais, PaisAdmin)
admin.site.register(Cidade, CidadeAdmin)
admin.site.register(CidadeDespesa, CidadeDespesaAdmin)
