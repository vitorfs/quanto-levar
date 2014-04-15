from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from core.models import *

def home(request):
    cidades = Cidade.objects.all()
    json = '['
    for cidade in cidades:
         json += '"'+cidade.nome+'",'
    json = json[:-1]
    json += ']'
    return render(request, 'core/home.html', {"cidades": json})

@require_POST
def buscar(request):
    try:
        nome_cidade = request.POST['cidade']
        cidade = Cidade.objects.get(nome__iexact=nome_cidade)
        url = u'/{0}/'.format(cidade.slug)
        return redirect(url)
    except Exception, e:
        return redirect('/')

def cidade(request, slug):
    cidade = Cidade.objects.get(slug=slug)
    despesas = CidadeDespesa.objects.filter(cidade__slug=slug)
    return render(request, 'core/cidade.html', {
        'despesas': despesas, 
        'cidade': cidade
        })

def calculo(request):
    cidade = request.POST.get('cidade')
    dias = request.POST.get('dias')
    nivel = request.POST.get('nivel')
    despesas_selecionadas = request.POST.getlist('despesas_selecionadas')
    lista_valores = {}
    for despesa in despesas_selecionadas:
        info = CidadeDespesa.objects.get(cidade=cidade, despesa=despesa, nivel=nivel)
        sigla = info.cidade.pais.cotacao.sigla
        cotacao = info.cidade.pais.cotacao.valor
        if sigla in lista_valores:
            lista_valores[sigla] += info.valor / cotacao
            lista_valores['BRL'] += info.valor
        else:
            lista_valores[sigla] = info.valor / cotacao
            lista_valores['BRL'] = info.valor
    cidade = Cidade.objects.get(pk=cidade)
    return render(request, 'core/calculo.html', {'valores': lista_valores, 'dias': dias, 'cidade': cidade.nome})