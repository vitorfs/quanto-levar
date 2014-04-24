from django import template
register = template.Library()

@register.filter
def dividir(valor, arg):
    try:
        valor = float(valor)
        arg = float(arg)
        if arg: return valor / arg
    except: pass
    return ''

@register.filter
def multiplicar(valor, arg):
    try:
        valor = float(valor)
        arg = float(arg)
        if arg: return valor * arg
    except: pass
    return ''

@register.filter
def somar_despesas(despesas, sigla):
    try:
        soma = 0
        for chave, valor in despesas.iteritems():
            if chave[1] == sigla:
                soma += valor
        return soma
    except: pass
    return ''