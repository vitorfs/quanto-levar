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
    despesas_selecionadas = request.GET.get('despesas_selecionadas')
    despesa = 100
    lista_valores = {"ARS": 0.22 * 100, "BRL": 100}
    return render(request, 'core/calculo.html', {'valores': lista_valores, 'dias': dias, 'cidade': cidade})