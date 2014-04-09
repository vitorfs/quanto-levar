from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'core.views.home', name='home'),
    url(r'^despesas/$', 'core.views.despesas', name='despesas'),
    url(r'^calculo/$', 'core.views.calculo', name='calculo'),
    url(r'^admin/', include(admin.site.urls)),
)
