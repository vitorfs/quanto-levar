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
    
def colabore(request):
    niveis = Nivel.objects.all()
    despesas = TipoDespesa.objects.all()
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
            resultado_alimentacao[despesa.tipo_despesa.nome] = [despesa.valor * cotacao.valor, despesa.valor]
        if categoria == TipoDespesa.TRANSPORTE:               
            resultado_transporte[despesa.tipo_despesa.nome] = [despesa.valor * cotacao.valor, despesa.valor]
        if categoria == TipoDespesa.HOSPEDAGEM:
            resultado_hospedagem[despesa.tipo_despesa.nome] = [despesa.valor * cotacao.valor, despesa.valor]
    for despesa, moedas in resultado_alimentacao.iteritems():
        if (u'BRL' and cotacao.sigla) in resultado_total:
            resultado_total[u'BRL'] += moedas[0]
            resultado_total[cotacao.sigla] += moedas[1] 
        else:
            resultado_total[u'BRL'] = moedas[0]
            resultado_total[cotacao.sigla] = moedas[1]
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

    print resultado_alimentacao
    print resultado_transporte
    print resultado_hospedagem
    print resultado_total
    return render(request, 'calculo.html', {'resultado_alimentacao': resultado_alimentacao, 'resultado_transporte': resultado_transporte, 'resultado_hospedagem': resultado_hospedagem, 'resultado_total': resultado_total, 'cotacao_sigla': cotacao.sigla, 'dias': dias, 'cidade': cidade})

#    dias = request.POST.get('dias')
#    nivel = request.POST.get('nivel')
#    despesas_selecionadas = request.POST.getlist('despesas-selecionadas')
#    cidade = Cidade.objects.get(slug=slug)
#    lista_valores = {}
#    transportes = {}
#    for despesa in despesas_selecionadas:
#        info = Despesa.objects.get(cidade=cidade, tipo_despesa=despesa, nivel=nivel)
#        sigla = info.cidade.pais.cotacao.sigla
#        cotacao = info.cidade.pais.cotacao.valor
#        categoria = info.despesa.categoria.nome
#        if categoria == "Hospedagem":
#            tipo_hospedagem = TipoDespesa.objects.get(id=despesa)
#        if categoria != "Transporte":
#            if categoria not in lista_valores:
#                lista_valores[categoria] = {}
#            if sigla in lista_valores[categoria]:
#                lista_valores[categoria][sigla] += info.valor
#                if sigla != 'BRL':
#                    lista_valores[categoria]['BRL'] += info.valor * cotacao
#            else:
#                lista_valores[categoria][sigla] = info.valor
#                if sigla != 'BRL':
#                    lista_valores[categoria]['BRL'] = info.valor * cotacao
#        else:
#            tipo_transporte = TipoDespesa.objects.get(id=despesa)
#            if tipo_transporte.nome not in transportes:
#                transportes[tipo_transporte.nome] = {}
#            transportes[tipo_transporte.nome][sigla] = info.valor
#            transportes[tipo_transporte.nome]['BRL'] = info.valor * cotacao
#    nivel = Nivel.objects.get(pk=nivel)
#    return render(request, 'calculo.html', {'resultado_alimentacao': lista_valores, 'dias': dias, 'cidade': cidade, 'nivel': nivel, 'transportes': transportes, 'tipo_hospedagem': tipo_hospedagem})

def carregar_cotacoes(request):
    Cotacao.atualizar_cotacao_banco_central()
    return HttpResponse()
