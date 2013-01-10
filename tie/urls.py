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

	url(r'^logout/$', 'principal.views.salir'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
   		{'document_root':settings.MEDIA_ROOT}
    ),


)
