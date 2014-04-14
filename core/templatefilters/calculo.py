from django import template
register = template.Library()

@register.filter
def dividir(valor, arg):
    try:
        valor = int(valor)
        arg = int(arg)
        if arg: return valor / arg
    except: pass
    return ''

@register.filter
def multiplicar(valor, arg):
    try:
        valor = int(valor)
        arg = int(arg)
        if arg: return valor * arg
    except: pass
    return ''