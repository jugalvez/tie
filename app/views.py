from django.http import HttpResponse
from django.utils import simplejson

def hola(request):

	response_data = {}
	response_data['result'] = 'failed'
	response_data['message'] = 'You Rock'
	a = simplejson.dumps(response_data)
	
	return HttpResponse(a, mimetype="application/json")