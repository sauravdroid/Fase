import hashlib
import hmac
import json
from random import random
import time
from django.http import JsonResponse
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
            return HttpResponse('Successfully Registered User')


@csrf_exempt
def citrus_return_url(request):
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

    if signature == request.POST.get('signature'):

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

    return_url = 'https://komorebitest.in/payments/citrus/return-url/'

    value = request.GET['amount']

    txnid = str(int(time.time())) + str(int(random.random() * 99999) + 10000);

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
