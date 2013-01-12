#encoding: utf-8

from django.contrib.auth.models import User
from principal.models import Cliente, Facturacion, Visita, Venta, Pago, Inventario, Pedido, Pago_Producto, Agenda
from django.contrib.auth import login as auth_login, authenticate, logout
from django.http import HttpResponse
from django.utils import simplejson
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
def hola(request):
	
	respuesta = {}
	respuesta['mensaje'] = 'Nada'

	if request.method == 'POST':

		user = request.POST.get('user')
		password = request.POST.get('pass')

		acceso = authenticate(username = user, password = password)

		if acceso is not None:
			if acceso.is_active:
				usuario = User.objects.get(username = user)
				respuesta['estatus'] = 200
				respuesta['mensaje'] = usuario.id

			else:
				respuesta['estatus'] = 500
				respuesta['mensaje'] = 'Tu cuenta no esta activa'

		else:
			respuesta['estatus'] = 400
			respuesta['mensaje'] = 'Ups, error de usuario o contraseña'

	json = simplejson.dumps(respuesta)
			
	return HttpResponse(json, mimetype="application/json")


@csrf_exempt
def clientes(request):

	respuesta = {}
	respuesta['mensaje'] = 'Nada'

	if request.method == 'POST':
		id_usuario = request.POST.get('id')

		clientes = Cliente.objects.filter(usuario_id = id_usuario)

		respuesta['estatus'] = 200
		respuesta['mensaje'] = serializers.serialize('json', clientes)

	json = simplejson.dumps(respuesta)
			
	return HttpResponse(json, mimetype="application/json")
