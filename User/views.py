from django.shortcuts import render
from django.shortcuts import HttpResponse


# Create your views here.
def index(request):
    if request.method == 'GET':
        return render(request,'User/index.html',{})
    else:
        username = request.POST.get('username','invalid')
        password = request.POST.get('password','invalid')
        return HttpResponse('Username = '+username + ' , Password = ' + password)
