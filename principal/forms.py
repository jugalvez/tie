#encoding: utf-8
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from principal.models import Cliente, Facturacion, Visita, Venta, Pago, Inventario, Pedido, Pago_Producto, Agenda

class DatosForm(forms.Form):
	nombre = forms.CharField(max_length = 30)
	apellido = forms.CharField(max_length = 30)
	email = forms.EmailField(max_length = 75)

	#nombre = forms.CharField(max_length=80, label='Titulo de la Galería', widget=forms.TextInput(attrs={'class':'special', 'placeholder': 'ejem. En la boda de mi mejor amigo'}))

class ClienteForm(ModelForm):
	class Meta:
		model = Cliente
		#exclude = ('usuario', 'estatus', 'tipo_venta', )

class FacturacionForm(ModelForm):
	class Meta:
		model = Facturacion		
		#exclude = ('cliente')

class AgendaForm(ModelForm):
	class Meta:
		model = Agenda