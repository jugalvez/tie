from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
	empresa = models.CharField(max_length = 80)
	nombre = models.CharField(max_length = 80)
	telefono = models.CharField(max_length = 25, blank = True, null = True)
	celular = models.CharField(max_length = 25, blank = True, null = True)
	radio = models.CharField(max_length = 25, blank = True, null = True)
	mail = models.EmailField(max_length = 75, blank = True, null = True)
	fecha_alta = models.DateField(auto_now = True)
	nota = models.TextField(blank = True, null = True)
	estatus = models.BooleanField(default = 1)
	tipo_venta = models.BooleanField()
	usuario = models.ForeignKey(User)

	def __unicode__(self):
		return self.empresa


class Facturacion(models.Model):
	cliente = models.ForeignKey(Cliente)
	rfc = models.CharField(max_length = 20, blank = True, null = True)
	calle = models.CharField(max_length = 80, blank = True, null = True)
	colonia = models.CharField(max_length = 80, blank = True, null = True)
	cp = models.IntegerField(max_length = 10, blank = True, null = True)
	municipio = models.CharField(max_length = 80, blank = True, null = True)
	estado = models.CharField(max_length = 35, blank = True, null = True)
	giro_comercial = models.CharField(max_length = 60, blank = True, null = True)

	def __unicode__(self):
		return self.cliente.empresa


class Visita(models.Model):
	titulo = models.CharField(max_length = 50)
	nota = models.TextField()
	estatus = models.BooleanField()
	lat = models.FloatField()
	lon = models.FloatField()
	fecha = models.DateField(auto_now = True)
	cliente = models.ForeignKey(Cliente)

	def __unicode__(self):
		return self.titulo


class Venta(models.Model):
	titulo = models.CharField(max_length = 80)
	detalle = models.TextField(blank = True, null = True)
	costo_produccion = models.FloatField(blank = True, default = 0)
	precio_venta = models.FloatField(blank = True, default = 0)
	fecha_entrega = models.DateField(blank = True, null = True)
	lat = models.FloatField()
	lon = models.FloatField()
	cliente = models.ForeignKey(Cliente)

	def __unicode__(self):
		return self.titulo


class Pago(models.Model):
	venta = models.ForeignKey(Venta)
	pago = models.FloatField(blank = True, default = 0)
	lat = models.FloatField()
	lon = models.FloatField()

	def __unicode__(self):
		return self.pago


class Inventario(models.Model):
	nombre = models.CharField(max_length = 200)
	imagen = models.ImageField(upload_to='catalogo')
	cantidad_total = models.IntegerField()
	costo_inicial = models.FloatField()
	precio_venta = models.FloatField()
	detalle = models.TextField(blank = True, null = True)
	usuario = models.ForeignKey(User)

	def __unicode__(self):
		return self.nombre


class Pedido(models.Model):
	producto = models.ForeignKey(Inventario)
	cantidad = models.FloatField()
	fecha = models.DateField(auto_now = True)
	cliente = models.ForeignKey(Cliente)
	lat = models.FloatField()
	lon = models.FloatField()
		
	def __unicode__(self):
		return self.producto.nombre


class Pago_Producto(models.Model):
	fecha_venta = models.DateField()
	pago = models.FloatField(default = 0)
	cliente = models.ForeignKey(Cliente)
	lat = models.FloatField()
	lon = models.FloatField()

	def __unicode__(self):
		return fecha_venta


class Agenda(models.Model):
	asunto = models.CharField(max_length = 60)
	detalle = models.TextField()
	fecha = models.DateField()
	hora = models.CharField(max_length = 10)
	cliente = models.ForeignKey(Cliente)

	def __unicode__(self):
		return self.asunto







