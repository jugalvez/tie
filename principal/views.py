from django.contrib.auth.models import User
from principal.models import Cliente, Facturacion, Visita, Venta, Pago, Inventario, Pedido, Pago_Producto, Agenda
from principal.forms import DatosForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate, logout

from django.contrib.auth.decorators import login_required


from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt



def inicio(request):
	return render_to_response('inicio.html', context_instance = RequestContext(request))


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
	
	usuario = User.objects.get(id = request.user.id)

	if request.method == 'POST':
		formulario = DatosForm(request.POST)

		if formulario.is_valid:
			nombre = request.POST['nombre']
			apellido = request.POST['apellido']
			mail = request.POST['email']


			usuario.update(first_name = nombre, last_name = apellido, email = mail)

	formulario = DatosForm(request.POST)
		
	return render_to_response('datos.html', {'formulario': formulario, 'usuario': usuario}, context_instance=RequestContext(request))



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