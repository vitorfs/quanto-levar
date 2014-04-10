from django.shortcuts import render
from core.models import *

def home(request):
    return render(request, 'core/home.html')

def despesas(request):
    cidade = request.GET.get('cidade')
    lista_despesas = CidadeDespesa.objects.filter(cidade=cidade)
    return render(request, 'core/despesas.html', {'despesas': lista_despesas, "cidade": cidade})

def calculo(request):
    cidade = request.GET.get('cidade')
    dias = request.GET.get('dias')
    nivel = request.GET.get('nivel')
    despesas_selecionadas = request.GET.get('despesas_selecionadas')
    for despesa in despesas_selecionadas:
        info = CidadeDespesa.objects.filter(cidade=cidade, despesa=despesa, nivel=nivel)
        print info
        print info.cidade
        sigla = info.cidade.pais.cotacao.sigla
        cotacao = info.cidade.pais.cotacao.valor
        lista_valores.update({sigla, cotacao * info.valor})
    return render(request, 'core/calculo.html', {'valores': lista_valores, 'dias': dias, 'cidade': cidade})