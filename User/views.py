from django.shortcuts import render
from django.shortcuts import HttpResponse


# Create your views here.
def index(request):
    if request.method == 'GET':
        return HttpResponse('Hello World')
    else:
        return HttpResponse('This is a post request')