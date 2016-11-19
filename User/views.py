import string
import hashlib
import hmac
import json
from .models import CitrusResponse
from .models import Seller,FavoriteShop
from .models import User
import time
from django.http import JsonResponse
from django.shortcuts import render,get_object_or_404
from django.shortcuts import HttpResponse
from django.http import HttpResponseBadRequest
from django.utils.crypto import random
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
            return HttpResponse('Successfully Registered User')


def is_app_token_valid(app_token):
    #code to check token
    return True

@csrf_exempt
def seller_register(request):
     if request.method =='POST':
         app_token=request.POST.get("APP_TOKEN")
         if(is_app_token_valid(app_token)):
           s_username=request.POST.get("username")
           s_password=request.POST.get("password")
           s_company_name=request.POST.get("cname")
           s_address=request.POST.get("address")
           s_phone_csv=request.POST.get("phone")
           s_city=request.POST.get("city")
           s_state=request.POST.get("state")
           s_pincode=int(request.POST.get("pincode"))

           #validation if needed  done here

           user=User()
           user.username=s_username
           user.set_password(s_password)
           user.save()
           seller = Seller()
           seller.seller=user
           seller.company_name=s_company_name
           seller.adress=s_address
           seller.phone_no=s_phone_csv
           seller.pincode=s_pincode
           seller.city=s_city
           seller.state=s_state
           seller.save()
           return HttpResponse("{ status:success,details:seller registration success}")
         else:
             return HttpResponse("{ status:fail,details:Invalid App Token}")
     else:
         #return HttpResponseBadRequest("{status:wrong method}")
         return HttpResponse("error")



@csrf_exempt
def setFavoriteShop(request):
    if request.method == 'POST':
        app_token = request.POST.get("APP_TOKEN")
        if (is_app_token_valid(app_token)):
            cusername = request.POST.get("username")
            merchant_id=request.POST.get("merchant_id")
            user=get_object_or_404(User,username=cusername)
            seller=get_object_or_404(Seller,pk=merchant_id)
            fShop=FavoriteShop()
            fShop.user=user
            fShop.fseller=seller
            fShop.tag=user.username+seller.company_name
            fShop.save()
            return HttpResponse("{ status:success,details:seller registration success}")
        else:
            return HttpResponse("{ status:fail,details:Invalid App Token}")
    else:
        # return HttpResponseBadRequest("{status:wrong method}")
        return HttpResponse("error")

@csrf_exempt
def getFavoriteShop(request):
    if request.method == 'GET':
        app_token = request.GET.get("APP_TOKEN")
        if (is_app_token_valid(app_token)):
            cusername=request.GET.get("username")
            fShops=FavoriteShop.objects.filter(user=User.objects.get(username=cusername))
            total=fShops.count()
            return HttpResponse("{ status:success,details:number of favorite shop "+str(total)+" }")
        else:
            return HttpResponse("{ status:fail,details:Invalid App Token}")
    else:
        # return HttpResponseBadRequest("{status:wrong method}")
        return HttpResponse("error")
@csrf_exempt
def citrus_return_url(request):
    citus_response = CitrusResponse()
    secret_key = "d1e4287f9b4d413b7c7286b9fd02dbdabeacf1ff"
    if request.method == 'GET':
        return HttpResponse("This is the Citrus Return Url.Post request should be sent here")
    if request.method == 'POST':
        data_string = (request.POST.get('TxId') + request.POST.get('TxStatus') +

                       request.POST.get('amount') + request.POST.get('pgTxnNo') +

                       request.POST.get('issuerRefNo') + request.POST.get('authIdCode') +

                       request.POST.get('firstName') + request.POST.get('lastName') +

                       request.POST.get('pgRespCode') + request.POST.get('addressZip'))

        signature = hmac.new(secret_key, data_string, hashlib.sha1).hexdigest()
        citus_response.data_string = data_string
        citus_response.transaction_id = request.POST.get('TxId')
    if signature == request.POST.get('signature'):
        citus_response.response_String = "<html> <head>< body><script>CitrusResponse.pgResponse('" + json.dumps(
            request.POST) + "');</script></body></head></html>"
        citus_response.save()
        return HttpResponse("<html> <head>< body><script>CitrusResponse.pgResponse('" + json.dumps(
            request.POST) + "');</script></body></head></html>")

    else:
        error = {"error": "Transaction Failed", "message": "Signature Verification Failed"}

    return HttpResponse(
        "<html> <head><body><script>CitrusResponse.pgResp onse('" + json.dumps(
            error) + "');<script></body></head></html>")


def citrus_bill_generator(request):
    access_key = "Q52UC15GP9QQXUW2UJHN"

    secret_key = "d1e4287f9b4d413b7c7286b9fd02dbdabeacf1ff"

    return_url = 'https://fase.herokuapp.com/returnurl'

    value = request.GET['amount']

    txnid = str(int(time.time())) + str(int(random.random() * 99999) + 10000)

    data_string = ('merchantAccessKey=' + access_key +

                   '&transactionId=' + txnid +

                   '&amount=' + value)

    signature = hmac.new(secret_key, data_string, hashlib.sha1).hexdigest()

    amount = {"value": value, "currency": 'INR'}

    bill = {

        "merchantTxnId": txnid,

        "amount": amount,

        "requestSignature": signature,

        "merchantAccessKey": access_key,

        "returnUrl": return_url

    }

    return JsonResponse(bill)
