from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'core.views.home', name='home'),
    url(r'^buscar/$', 'core.views.buscar', name='buscar'),
    url(r'^colaborar/$', 'core.views.colaborar', name='colaborar'),
    url(r'^enviar/$', 'core.views.enviar', name='enviar'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<slug>[-\w]+)/calculo/$', 'core.views.calculo', name='calculo'),
    url(r'^(?P<slug>[-\w]+)/$', 'core.views.cidade', name='cidade'),
)
