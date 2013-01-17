#encoding: utf-8

from django.contrib.auth.models import User
from django.db.models import Sum
from principal.models import Cliente, Facturacion, Visita, Venta, Pago, Inventario, Pedido, Pago_Producto, Agenda
from django.contrib.auth import login as auth_login, authenticate, logout
from django.http import HttpResponse
from django.utils import simplejson
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
def hola(request):
	
	respuesta = {}
	respuesta['estatus'] = '400'

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
			
	return HttpResponse(json, mimetype = "application/json")


@csrf_exempt
def clientes(request):
	respuesta = {}
	respuesta['estatus'] = '400'

	if request.method == 'POST':
		id_usuario = request.POST.get('id')

		clientes = Cliente.objects.filter(usuario_id = id_usuario).order_by('nombre')

		respuesta['estatus'] = 200
		respuesta['mensaje'] = serializers.serialize('json', clientes)

	json = simplejson.dumps(respuesta)
			
	return HttpResponse(json, mimetype = "application/json")



@csrf_exempt
def nuevoCliente(request):
	respuesta = {}
	respuesta['estatus'] = 400

	if request.method == 'POST':

		empresa = request.POST.get('empresa')
		nombre = request.POST.get('nombre')
		telefono = request.POST.get('telefono')
		celular = request.POST.get('movil')
		radio = request.POST.get('otro')
		mail = request.POST.get('mail')
		nota = request.POST.get('nota')
		usuario = request.POST.get('id')

		cliente = Cliente(empresa = empresa, nombre = nombre, telefono = telefono, celular = celular, radio = radio, mail = mail, nota = nota, usuario_id = usuario, estatus = 1, tipo_venta = 0)
		cliente.save()
	
		respuesta['estatus'] = 200

	json = simplejson.dumps(respuesta)

	return HttpResponse(json, mimetype = "application/json")




@csrf_exempt
def agenda(request):
	respuesta = {}
	respuesta['estatus'] = 400

	if request.method == 'POST':
		id_usuario = request.POST.get('id')

		agenda = Agenda.objects.filter(usuario_id = id_usuario).order_by('-id')

		respuesta['estatus'] = 200
		respuesta['mensaje'] = serializers.serialize('json', agenda)

	json = simplejson.dumps(respuesta)
			
	return HttpResponse(json, mimetype = "application/json")


@csrf_exempt
def nuevoEvento(request):
	respuesta = {}
	respuesta['estatus'] = 400

	if request.method == 'POST':
		asunto = request.POST.get('asunto')
		detalle = request.POST.get('detalle')
		fecha = request.POST.get('fecha')
		hora = request.POST.get('hora')
		cliente = request.POST.get('cliente')
		usuario = request.POST.get('id')

		agenda = Agenda(asunto = asunto, detalle = detalle, fecha = fecha, hora = hora, cliente_id = cliente, usuario_id = usuario)
		agenda.save()
		respuesta['estatus'] = 200

	json = simplejson.dumps(respuesta)

	return HttpResponse(json, mimetype = "application/json")



@csrf_exempt
def visita(request):
	respuesta = {}
	respuesta['estatus'] = 400

	if request.method == 'POST':
		asunto = request.POST.get('asunto')
		detalle = request.POST.get('detalle')
		estatus = request.POST.get('estatus')
		lat = request.POST.get('lat')
		lng = request.POST.get('lng')
		cliente	= request.POST.get('cliente')
		usuario= request.POST.get('id')

		visita = Visita(titulo = asunto, nota = detalle, estatus = estatus, lat = lat, lon = lng, cliente_id = cliente, usuario_id = usuario)
		visita.save()
		respuesta['estatus'] = 200

	json = simplejson.dumps(respuesta)

	return HttpResponse(json, mimetype = "application/json")


@csrf_exempt
def venta(request):
	respuesta = {}
	respuesta['estatus'] = 400

	if request.method == 'POST':
		titulo = request.POST.get('titulo')
		detalle = request.POST.get('detalle')
		fecha = request.POST.get('fecha')
		cliente	= request.POST.get('cliente')
		costo	= request.POST.get('costo')
		lat = request.POST.get('lat')
		lng = request.POST.get('lng')
		usuario= request.POST.get('id')

		venta = Venta(titulo = titulo, detalle = detalle, precio_venta = costo, fecha_entrega = fecha, lat = lat, lon = lng , cliente_id = cliente, usuario_id = usuario)
		venta.save()
		pago = Pago(venta = venta.id, pago = 0, lat = lat, lon = lng)
		pago.save()

		respuesta['estatus'] = 200

	json = simplejson.dumps(respuesta)

	return HttpResponse(json, mimetype = "application/json")




@csrf_exempt
def trabajos(request):
	respuesta = {}
	respuesta['estatus'] = 400

	if request.method == 'POST':
		id_usuario = request.POST.get('id')
		id_cliente = request.POST.get('cliente')

		venta = Venta.objects.filter(usuario_id = id_usuario, cliente_id = id_cliente).order_by('-id')
		total = len(venta)

		respuesta['estatus'] = 200
		respuesta['mensaje'] = serializers.serialize('json', venta)
		respuesta['total'] = total

	json = simplejson.dumps(respuesta)
			
	return HttpResponse(json, mimetype = "application/json")



@csrf_exempt
def cobros(request):
	respuesta = {}
	respuesta['estatus'] = 400

	if request.method == 'POST':
		id_venta = request.POST.get('venta')
		venta = Venta.objects.get(pk = id_venta)
		restante = Pago.objects.filter(venta_id = id_venta)

		suma = 0
		for resta in restante:
			suma = suma+resta.pago


		respuesta['estatus'] = 200
		respuesta['cliente'] = venta.cliente.empresa
		respuesta['titulo'] = venta.titulo
		respuesta['detalle'] = venta.detalle
		respuesta['total'] = venta.precio_venta
		respuesta['restante'] = suma

	json = simplejson.dumps(respuesta)

	return HttpResponse(json, mimetype = "application/json")


@csrf_exempt
def nuevoCobro(request):
	respuesta = {}
	respuesta['estatus'] = 400
	
	if request.method == 'POST':
		id_venta = request.POST.get('venta')
		pago = request.POST.get('cobro')
		lat = request.POST.get('lat')
		lng = request.POST.get('lng')

		pago = Pago(venta_id = id_venta, pago = pago, lat = lat, lon = lng)
		pago.save()

	respuesta['estatus'] = 200

	json = simplejson.dumps(respuesta)

	return HttpResponse(json, mimetype = "application/json")
