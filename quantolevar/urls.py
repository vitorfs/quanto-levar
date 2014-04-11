from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'core.views.home', name='home'),
    url(r'^buscar/$', 'core.views.buscar', name='buscar'),
    url(r'^calculo/$', 'core.views.calculo', name='calculo'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<slug>[-\w]+)/$', 'core.views.cidade', name='cidade'),
)
