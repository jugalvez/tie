#encoding: utf-8

from django.contrib.auth.models import User
from principal.models import Cliente, Facturacion, Visita, Venta, Pago, Inventario, Pedido, Pago_Producto, Agenda
from principal.forms import DatosForm, ClienteForm, FacturacionForm, AgendaForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.decorators import login_required


from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt



def inicio(request):
	us = request.user
	return render_to_response('inicio.html', {'us': us} ,context_instance = RequestContext(request))


def login(request):
	if request.method == 'POST':
		formulario = AuthenticationForm(request.POST)

		if formulario.is_valid:
			usuario = request.POST['username']
			clave = request.POST['password']
			acceso = authenticate(username=usuario, password=clave)

			if acceso is not None:
				if acceso.is_active:
					auth_login(request, acceso)
					return HttpResponseRedirect('/panel')
				else:
					return render_to_response('noactivo.html', context_instance = RequestContext(request))
			else:
				return render_to_response('nousuario.html', context_instance = RequestContext(request))
	else:
		formulario = AuthenticationForm()
	return render_to_response('login.html', {'formulario': formulario}, context_instance = RequestContext(request))


def registro(request):
	if request.method == 'POST':
		formulario = UserCreationForm(request.POST)
		if formulario.is_valid:
			formulario.save()
			return HttpResponseRedirect('/')
	else:
		formulario = UserCreationForm()

	return render_to_response('registro.html', {'formulario': formulario}, context_instance = RequestContext(request))


@login_required(login_url='/login')
def panel(request):
	usuario = request.user
	return render_to_response('panel.html', {'usuario': usuario } ,context_instance = RequestContext(request))


@login_required(login_url='/login')
def datos(request):

	if request.method == 'POST':
		formulario = DatosForm(request.POST)

		if formulario.is_valid():
			nombre = request.POST['nombre']
			apellido = request.POST['apellido']
			mail = request.POST['email']
			
			usuario_update = User.objects.filter(id = request.user.id)
			usuario_update.update(first_name = nombre, last_name = apellido, email = mail)

	usuario = User.objects.get(id = request.user.id)
	formulario = DatosForm()
		
	return render_to_response('datos.html', {'formulario': formulario, 'usuario': usuario}, context_instance=RequestContext(request))


@login_required(login_url='/login')
def clientes(request):
	clientes = Cliente.objects.filter(usuario_id = request.user.id).order_by('empresa')
	return render_to_response('lista-clientes.html', {'clientes': clientes}, context_instance=RequestContext(request))


@login_required(login_url='/login')
def nuevoCliente(request):
	if request.method == 'POST':
		# Creamos un objeto para colocar campos manualmente, despues se lo asignamos al formulario que recibimos
		cliente = Cliente(usuario_id = request.user.id, estatus = 1, tipo_venta = 0)
		formulario = ClienteForm(request.POST, instance = cliente)

		#Si el formulario es valido, guardamos el nuevo registro; asignamos campos manualmente a FacturacionForm

		if formulario.is_valid():
			id_cliente = formulario.save()
			facturacion = Facturacion(cliente_id = id_cliente.id)
			facturacion.save()
		
			return HttpResponseRedirect('/clientes')
	else:
		formulario = ClienteForm()
		form_facturacion = FacturacionForm()

	return render_to_response('nuevo-cliente.html', {'formulario': formulario}, context_instance=RequestContext(request))


@login_required(login_url='/login')
def editarCliente(request, id_cliente):
	
	Qform = Cliente.objects.get(pk = id_cliente)
	Qform_facturacion = Facturacion.objects.get(cliente_id = id_cliente)

	if request.method == 'POST':
		# Recibimos el ID del cliente, lo buscamos en la BD, asignamos al Form y actualizamos
		idPost = request.POST.get('id')
		Qform = Cliente.objects.get(pk = idPost)
		formulario = ClienteForm(request.POST, instance = Qform)

		#Si el formulario es valido, actualizamos el nuevo registro; asignamos campos manualmente a FacturacionForm
		if formulario.is_valid():
			formulario.save()

			facturacion = Facturacion.objects.get(cliente_id = idPost)
			form_facturacion = FacturacionForm(request.POST, instance = facturacion)

			if form_facturacion.is_valid():
				form_facturacion.save()		

		return HttpResponseRedirect('/clientes/editar/%d' % int(idPost))
	else:

		formulario = ClienteForm(instance = Qform)
		form_facturacion = FacturacionForm(instance = Qform_facturacion)

	return render_to_response('nuevo-cliente.html', {'formulario': formulario, 'form_facturacion': form_facturacion, 'cliente': id_cliente}, context_instance=RequestContext(request))


@login_required(login_url='/login')
def eliminarCliente(request, id_cliente):
	borra = Cliente.objects.get(pk = id_cliente)
	borra.delete()

	return HttpResponseRedirect('/clientes/')


@login_required(login_url='/login')
def agenda(request):
	eventos = Agenda.objects.filter(usuario_id = request.user.id).order_by('-fecha')
	return render_to_response('agenda.html', {'eventos': eventos}, context_instance=RequestContext(request))


@login_required(login_url='/login')
def nuevoEvento(request):
	if request.method == 'POST':
		agenda = Agenda(usuario_id = request.user.id)
		formulario = AgendaForm(request.POST, instance = agenda)

		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect('/agenda')
	else:
		formulario = AgendaForm()

	return render_to_response('nuevo-evento.html', {'formulario': formulario}, context_instance=RequestContext(request))



@login_required(login_url='/login')
def estadisticasVisitas(request, id_cliente):
	visitas = Visita.objects.filter(cliente = id_cliente).order_by('-fecha')
	#buenas = Visita.objects.extra(select = { 'total': 'SELECT count(*) FROM principal_visita WHERE estatus = 1 GROUP BY fecha'})
	cliente = Cliente.objects.get(pk = id_cliente)

	return render_to_response('estadisticas-visitas.html', {'cliente': cliente, 'visitas': visitas}, context_instance=RequestContext(request))


@login_required(login_url='/login')
def estadisticasVentas(request, id_cliente):
	ventas = Venta.objects.filter(cliente = id_cliente).order_by('-pk')
	cliente = Cliente.objects.get(pk = id_cliente)

	return render_to_response('estadisticas-ventas.html', {'cliente': cliente, 'ventas': ventas}, context_instance=RequestContext(request))


@login_required(login_url='/login')
def estadisticasCobros(request, id_cliente):
	ventas = Venta.objects.filter(cliente = id_cliente).order_by('-pk')
	cobros = Pago.objects.filter(venta_id = ventas).order_by('venta')
	cliente = Cliente.objects.get(pk = id_cliente)

	return render_to_response('estadisticas-cobros.html', {'cliente': cliente, 'cobros': cobros}, context_instance=RequestContext(request))



@login_required(login_url='/login')
def salir(request):
	logout(request)
	return HttpResponseRedirect('/')







'''
		if form.is_valid():
			usuario = form.cleaned_data['usuario']
			password = form.cleaned_data['password']
			nombre = form.cleaned_data['nombre']
			apellido = form.cleaned_data['apellido']
			email = form.cleaned_data['email']

			nuevo_usuario = User(
				username = usuario,
				password = password,
				first_name = nombre,
				last_name = apellido,
				email = email
			)

			nuevo_usuario.save()

			return HttpResponseRedirect('/')
'''	