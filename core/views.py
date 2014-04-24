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
    return render(request, 'cidade.html', {'cidade': cidade})
    
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
        categoria = info.despesa.categoria.nome
        if categoria not in lista_valores:
            lista_valores[categoria] = {}
        if sigla in lista_valores[categoria]:
            lista_valores[categoria][sigla] += info.valor
            if sigla != 'BRL':
                lista_valores[categoria]['BRL'] += info.valor * cotacao
        else:
            lista_valores[categoria][sigla] = info.valor
            if sigla != 'BRL':
                lista_valores[categoria]['BRL'] = info.valor * cotacao
    nivel = Nivel.objects.get(pk=nivel)
    return render(request, 'calculo.html', {'valores': lista_valores, 'dias': dias, 'cidade': cidade, 'nivel': nivel})

def carregar_cotacoes(request):
    Cotacao.atualizar_cotacao_banco_central()
    return HttpResponse()
