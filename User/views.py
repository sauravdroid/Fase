from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import *


# Create your views here.
@csrf_exempt
def index(request):
    if request.method == 'GET':
        return render(request, 'User/index.html', {})
    else:
        username = request.POST.get('username', 'Empty')
        password = request.POST.get('password', 'Empty')
        return HttpResponse('Username = ' + username + ' , Password = ' + password)


@csrf_exempt
def user_register(request):
    if request.method == 'GET':
        form = FaseUserForm()
        return render(request, 'User/register.html', {'form': form})
    else:
        form = FaseUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            return HttpResponse('Successfully Registered')
