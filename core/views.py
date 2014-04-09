from django.shortcuts import render
from core.models import *

def home(request):
    return render(request, 'core/home.html')

def despesas(request):
    if not Despesa.objects.all():
        Despesa(tipo="Teste1").save()
        Despesa(tipo="Teste2").save()
        Despesa(tipo="Teste3").save()
        Despesa(tipo="Teste4").save()
    lista_despesas = Despesa.objects.all()
    return render(request, 'core/despesas.html', {'despesas': lista_despesas})