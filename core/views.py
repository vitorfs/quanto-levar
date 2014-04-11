from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from core.models import *

def home(request):
    return render(request, 'core/home.html')

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
    cidade = request.GET.get('cidade')
    dias = request.GET.get('dias')
    nivel = request.GET.get('nivel')
    despesas_selecionadas = request.GET.get('despesas_selecionadas')
    for despesa in despesas_selecionadas:
        info = CidadeDespesa.objects.get(cidade=cidade, despesa=despesa, nivel=nivel)
        print info
        print info.cidade
        sigla = info.cidade.pais.cotacao.sigla
        cotacao = info.cidade.pais.cotacao.valor
        lista_valores = {sigla : cotacao * info.valor }
    return render(request, 'core/calculo.html', {'valores': lista_valores, 'dias': dias, 'cidade': cidade})