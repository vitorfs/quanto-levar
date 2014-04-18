# coding: utf-8

from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from core.decorators import ajax_required
from recaptcha.client import captcha
from core.models import *

def json_cidades():
    cidades = []
    for cidade in Cidade.objects.all(): 
        cidades.append(u'"{0}"'.format(cidade.nome))
    return u'[{0}]'.format(','.join(cidades))

def home(request):
    return render(request, 'busca.html', {'cidades': json_cidades()})

def cidade(request, slug):
    cidade = Cidade.objects.get(slug=slug)
    cidade_despesas = CidadeDespesa.objects.filter(cidade=cidade)
    niveis = Nivel.objects.filter(id__in=cidade_despesas.values("nivel").distinct())
    niveis_despesas = {}
    for nivel in niveis:
        niveis_despesas[nivel.id] = filter(lambda despesa: despesa.nivel.id == nivel.id, cidade_despesas)
    return render(request, 'cidade.html', {'niveis_despesas': niveis_despesas, 'cidade': cidade, 'niveis': niveis})
    
@ajax_required
@require_POST
def buscar(request):
    nome_cidade = request.POST['cidade']
    try:
        cidade = Cidade.objects.get(nome__iexact=nome_cidade)
        url = u'/{0}/'.format(cidade.slug)
        return HttpResponse(url)
    except Exception, e:
        return HttpResponseBadRequest(u'Não encontramos nenhum registro para a cidade {0} :('.format(nome_cidade))
    
def colabore(request):
    niveis = Nivel.objects.all()
    despesas = Despesa.objects.all()
    return render(request, 'colabore.html', {'niveis': niveis, 'despesas': despesas})

@require_POST
def enviar(request):
    cidade = request.POST['cidade']
    estado = request.POST['estado']
    print cidade
    print estado
    
    if request.method == 'POST':
        response = captcha.submit(
        request.POST['recaptcha_challenge_field'],
        request.POST['recaptcha_response_field'],
        "6Lew2fESAAAAAKz04iu27K1TTXTDw-j5LlXqkiwE",
        request.META.get('REMOTE_ADDR'))
    if not response.is_valid:
        print "INVALID!"
    else:
        print "VALID!"
    return render(request, 'colabore.html')

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

def carregar_cotacoes(request):
    Cotacao.atualizar_cotacao_banco_central()
    return HttpResponse()