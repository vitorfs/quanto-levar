# coding: utf-8

from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from core.decorators import ajax_required
from recaptcha.client import captcha
from core.models import *
from django.db.models import Q

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

@ajax_required
@require_POST
def validar_captcha(request):
    captcha_response = captcha.submit(
    request.POST['recaptcha_challenge_field'],
    request.POST['recaptcha_response_field'],
    "6Lew2fESAAAAAKz04iu27K1TTXTDw-j5LlXqkiwE",
    request.META.get('REMOTE_ADDR'))    
    if captcha_response.is_valid:
        return HttpResponse('True')
    else:
        return HttpResponse('False')

def colabore(request):
    if request.method == 'POST':
        descricao = u''
        for key, value in request.POST.iteritems():
            descricao += u'{0}: {1}\n'.format(key, value)
        Colaboracao(descricao=descricao).save()
        return render(request, 'sucesso.html')
    else:
        despesas = TipoDespesa.objects.all().order_by("id")
        print despesas
        return render(request, 'colabore.html', {'despesas': despesas})

@require_POST
def calculo(request, slug):
    cidade = get_object_or_404(Cidade, slug=slug)

    dias = request.POST.get('dias')
    nivel = request.POST.get('nivel')
    alimentacao = request.POST.getlist('alimentacao')
    transporte = request.POST.getlist('transporte')
    hospedagem = request.POST.get('hospedagem')

    tipos_despesas = alimentacao + transporte + list(hospedagem)
    despesas = Despesa.objects.filter(tipo_despesa__id__in=tipos_despesas).filter(Q(nivel=nivel, cidade=cidade) | Q(nivel=None))
    
    cotacao = cidade.pais.cotacao
    
    resultado_alimentacao = {}
    resultado_transporte = {}
    resultado_hospedagem = {}
    resultado_total = {}        
    for despesa in despesas:
        categoria = despesa.tipo_despesa.categoria
        if categoria == TipoDespesa.ALIMENTACAO:
            resultado_alimentacao[str(despesa.tipo_despesa.id) + despesa.tipo_despesa.nome] = [despesa.valor * cotacao.valor, despesa.valor]
        if categoria == TipoDespesa.TRANSPORTE:               
            resultado_transporte[despesa.tipo_despesa.nome] = [despesa.valor * cotacao.valor, despesa.valor]
        if categoria == TipoDespesa.HOSPEDAGEM:
            resultado_hospedagem[despesa.tipo_despesa.nome] = [despesa.valor * cotacao.valor, despesa.valor]
    if resultado_alimentacao:
        for despesa, moedas in resultado_alimentacao.iteritems():
            if (u'BRL' and cotacao.sigla) in resultado_total:
                resultado_total[u'BRL'] += moedas[0]
                resultado_total[cotacao.sigla] += moedas[1] 
            else:
                resultado_total[u'BRL'] = moedas[0]
                resultado_total[cotacao.sigla] = moedas[1]
    if resultado_hospedagem:
        for despesa, moedas in resultado_hospedagem.iteritems():
            if (u'BRL' and cotacao.sigla) in resultado_total:
                resultado_total[u'BRL'] += moedas[0]
                resultado_total[cotacao.sigla] += moedas[1] 
            else:
                resultado_total[u'BRL'] = moedas[0]
                resultado_total[cotacao.sigla] = moedas[1]            
    if nivel == Despesa.ECONOMICO:
        print "metrica para transporte em economico"
    if nivel == Despesa.MODERADO:
        print "metrica para transporte em moderado"
    if nivel == Despesa.CARO:
        print "metrica para transporte em caro"

    resultado_alimentacao = sorted(resultado_alimentacao.items())
    return render(request, 'calculo.html', {'resultado_alimentacao': resultado_alimentacao, 'resultado_transporte': resultado_transporte, 'resultado_hospedagem': resultado_hospedagem, 'resultado_total': resultado_total, 'cotacao_sigla': cotacao.sigla, 'dias': dias, 'cidade': cidade})

def carregar_cotacoes(request):
    Cotacao.atualizar_cotacao_banco_central()
    return HttpResponse()
