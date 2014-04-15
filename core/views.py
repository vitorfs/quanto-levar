from django.http import HttpResponseBadRequest
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
    return render(request, 'core/home.html', {"cidades": json_cidades()})

def cidade(request, slug):
    cidade = Cidade.objects.get(slug=slug)
    despesas = CidadeDespesa.objects.filter(cidade__slug=slug)
    return render(request, 'core/cidade.html', {'despesas': despesas, 'cidade': cidade})
    
@ajax_required
def buscar(request):
    if request.method == 'POST':
        try:
            nome_cidade = request.POST['cidade']
            cidade = Cidade.objects.get(nome__iexact=nome_cidade)
            despesas = CidadeDespesa.objects.filter(cidade=cidade)
            niveis = {}
            for despesa in despesas: 
                niveis[despesa.nivel.id] = despesa.nivel.nome
            print niveis
            return render(request, 'core/partial_cidade.html', {'despesas': despesas, 'cidade': cidade, 'niveis': niveis})
        except Exception, e:
            return HttpResponseBadRequest()
    else:
        return render(request, 'core/partial_busca.html', {"cidades": json_cidades()})

@ajax_required
def calculo(request):
    cidade = request.POST.get('cidade')
    dias = request.POST.get('dias')
    nivel = request.POST.get('nivel')
    despesas_selecionadas = request.POST.getlist('despesas-selecionadas')
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
    return render(request, 'core/partial_calculo.html', {'valores': lista_valores, 'dias': dias, 'cidade': cidade})
