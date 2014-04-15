from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from core.decorators import ajax_required
from core.models import *

def json_cidades():
    cidades = []
    for cidade in Cidade.objects.all(): 
        cidades.append(u'"{0}"'.format(cidade.nome))
    return u'[{0}]'.format(','.join(cidades))

def home(request):
    return render(request, 'busca.html', {"cidades": json_cidades()})

def cidade(request, slug):
    cidade = Cidade.objects.get(slug=slug)
    despesas = CidadeDespesa.objects.filter(cidade__slug=slug)
    niveis = {}
    for despesa in despesas: 
        niveis[despesa.nivel.id] = despesa.nivel.nome
    return render(request, 'cidade.html', {'despesas': despesas, 'cidade': cidade, 'niveis': niveis})
    
@ajax_required
@require_POST
def buscar(request):
    try:
        nome_cidade = request.POST['cidade']
        cidade = Cidade.objects.get(nome__iexact=nome_cidade)
        url = u'/{0}/'.format(cidade.slug)
        return HttpResponse(url)
    except Exception, e:
        return HttpResponseBadRequest()

@require_POST
def calculo(request, slug):
    dias = request.POST.get('dias')
    nivel = request.POST.get('nivel')
    despesas_selecionadas = request.POST.getlist('despesas-selecionadas')
    cidade = Cidade.objects.get(slug=slug)
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
    return render(request, 'calculo.html', {'valores': lista_valores, 'dias': dias, 'cidade': cidade})
