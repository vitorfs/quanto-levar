from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'core.views.home', name='home'),
    url(r'^buscar/$', 'core.views.buscar', name='buscar'),
    url(r'^colabore/(?P<slug>[-\w]+)$', 'core.views.colabore', name='colabore'),
    url(r'^sobre/$', 'core.views.sobre', name='sobre'),
    url(r'^validar_captcha/$', 'core.views.validar_captcha', name='validar_captcha'),
    url(r'^carregarcotacoes/$', 'core.views.carregar_cotacoes', name='carregar_cotacoes'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<slug>[-\w]+)/calculo/$', 'core.views.calculo', name='calculo'),
    url(r'^(?P<slug>[-\w]+)/$', 'core.views.cidade', name='cidade'),
)
