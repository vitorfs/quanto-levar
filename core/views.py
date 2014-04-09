from django.shortcuts import render
from core.models import *

def home(request):
    return render(request, 'core/home.html')

def despesas(request):
    lista_despesas = Despesa.objects.all()
    return render(request, 'core/despesas.html', {'despesas': lista_despesas})

def calculo(request):
    return render(request, 'core/calculo.html', {'calculo': ""})