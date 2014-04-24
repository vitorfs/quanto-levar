from django.contrib import admin
from core.models import *

class CotacaoAdmin(admin.ModelAdmin):
    list_display = ('sigla', 'valor',)
    search_fields = ['sigla',]
  
class DespesaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria',)
    list_filter = ['categoria',]

class CidadeInline(admin.TabularInline):
    model = Cidade
    fields = ['nome', 'estado']
    extra = 1
  
class PaisAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cotacao', 'codigo',)
    search_fields = ['cotacao__sigla', 'nome', 'codigo']
    inlines = [CidadeInline]

class CidadeDespesaInline(admin.TabularInline):
    model = CidadeDespesa
    fields = ['despesa', 'nivel', 'valor']
    extra = 1

class CidadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'estado', 'pais',)
    list_filter = ['pais',]
    search_fields = ['nome', 'estado', 'pais__nome']
    inlines = [CidadeDespesaInline]

admin.site.register(Cotacao, CotacaoAdmin)
admin.site.register(Despesa, DespesaAdmin)
admin.site.register(Pais, PaisAdmin)
admin.site.register(Cidade, CidadeAdmin)