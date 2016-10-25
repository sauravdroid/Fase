from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def index(request):
    if request.method == 'GET':
        return render(request,'User/index.html',{})
    else:
        username = request.POST.get('username','invalid')
        password = request.POST.get('password','invalid')
        return HttpResponse('Username = '+username + ' , Password = ' + password)
