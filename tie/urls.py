from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
	url(r'^$', 'principal.views.inicio'),
	url(r'^registro/$', 'principal.views.registro'),
	url(r'^login/$', 'principal.views.login'),
	url(r'^panel/$', 'principal.views.panel'),
	url(r'^datos/$', 'principal.views.datos'),
	url(r'^clientes/$', 'principal.views.clientes'),
	url(r'^clientes/nuevo/$', 'principal.views.nuevoCliente'),
	url(r'^agenda/$', 'principal.views.agenda'),
	url(r'^agenda/nuevo/$', 'principal.views.nuevoEvento'),


	
	url(r'^hola/$', 'app.views.hola'),
	url(r'^app/clientes/$', 'app.views.clientes'),
	url(r'^app/cliente/nuevo/$', 'app.views.nuevoCliente'),
	url(r'^app/agenda/$', 'app.views.agenda'),
	url(r'^app/agenda/nuevo/$', 'app.views.nuevoEvento'),
	url(r'^app/visita/nuevo/$', 'app.views.visita'),
	url(r'^app/venta/nuevo/$', 'app.views.venta'),
	url(r'^app/trabajos/$', 'app.views.trabajos'),
	url(r'^app/cobros/$', 'app.views.cobros'),
	url(r'^app/cobros/nuevo/$', 'app.views.nuevoCobro'),

	url(r'^logout/$', 'principal.views.salir'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
   		{'document_root':settings.MEDIA_ROOT}
    ),


)
