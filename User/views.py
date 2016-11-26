import hashlib
import hmac
import json
import time
from django.core import exceptions
from django.core.signing import Signer, BadSignature
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.crypto import random
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from .forms import *
from .models import CitrusResponse
from .models import Seller, FavoriteShop
from .serializer import SellerSeraialzer, AppSerializer, UserSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token


class ApiViewNew(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)


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


def is_app_token_valid(app_token):
    # code to check token
    print("token" + str(app_token))
    return True


@csrf_exempt
def seller_register(request):
    if request.method == 'POST':
        app_token = request.POST.get("APP_TOKEN")
        if (is_app_token_valid(app_token)):
            s_username = request.POST.get("username")
            s_password = request.POST.get("password")
            s_company_name = request.POST.get("cname")
            s_address = request.POST.get("address")
            s_phone_csv = request.POST.get("phone")
            s_city = request.POST.get("city")
            s_state = request.POST.get("state")
            s_pincode = int(request.POST.get("pincode"))

            # validation if needed  done here

            user = User()
            user.username = s_username
            user.set_password(s_password)
            user.save()
            seller = Seller()
            seller.seller = user
            seller.company_name = s_company_name
            seller.adress = s_address
            seller.phone_no = s_phone_csv
            seller.pincode = s_pincode
            seller.city = s_city
            seller.state = s_state
            seller.save()
            data = {}
            data["status"] = "success"
            data["details"] = "seller registration success"
            return JsonResponse(data)
        else:
            data = {}
            data["status"] = "fail"
            data["details"] = "Invalid App Token"
            return JsonResponse(data)
            # return HttpResponse("{ status:fail,details:Invalid App Token}")
    else:
        # return HttpResponseBadRequest("{status:wrong method}")
        data = {}
        data["status"] = "fail"
        data["details"] = "make a post request"
        return JsonResponse(data)


@csrf_exempt
def setFavoriteShop(request):
    if request.method == 'POST':
        app_token = request.POST.get("APP_TOKEN", "kjk")
        if (is_app_token_valid(app_token)):
            cusername = request.POST.get("username")
            merchant_id = int(request.POST.get("merchant_id"))
            user = get_object_or_404(User, username=cusername)
            seller = get_object_or_404(Seller, pk=merchant_id)
            fShop = FavoriteShop()
            fShop.user = user
            fShop.fseller = seller
            fShop.tag = user.username + seller.company_name
            fShop.save()
            data = {}
            data["status"] = "success"
            data["details"] = "favorite shop set"
            return JsonResponse(data)
        else:
            data = {}
            data["status"] = "fail"
            data["details"] = "Invalid App Token"
            return JsonResponse(data)

    else:
        # return HttpResponseBadRequest("{status:wrong method}")
        data = {}
        data["status"] = "fail"
        data["details"] = "make a post request"
        return JsonResponse(data)


class favshop(APIView):
    @csrf_exempt
    def getFavoriteShop(request):
        if request.method == 'GET':
            app_token = request.GET.get("APP_TOKEN")
            if (is_app_token_valid(app_token)):
                cusername = request.GET.get("username")
                try:
                    fShops = FavoriteShop.objects.filter(user=User.objects.get(username=cusername))
                    Shops = Seller.objects.filter(id__in=fShops.all().values('fseller'))
                    serialized = SellerSeraialzer(Shops, many=True)
                except exceptions.ObjectDoesNotExist:
                    data = {}
                    data["status"] = "fail"
                    data["details"] = "user does not exit"

                    return JsonResponse(data)
                return JsonResponse(serialized.data, safe=False)
            else:
                data = {}
                data["status"] = "fail"
                data["details"] = "Invalid App Token"
                return JsonResponse(data)
        else:
            # return HttpResponseBadRequest("{status:wrong method}")
            data = {}
            data["status"] = "fail"
            data["details"] = "make a post request"
            return JsonResponse(data)


@api_view(['POST'])
def create_app_api(request):
    if request.method == 'POST':
        signer = Signer(request.data['app_secret_key'])
        request.data['app_encrypted_key'] = signer.sign(request.data['app_name'])
        serializer = AppSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Response": "App Creation Successful", "Secret-Key": serializer.data['app_encrypted_key']})
        else:
            return Response({"Response": "Error Occured", "serializer": serializer.data},
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def create_app(request):
    if request.method == 'GET':
        form = CreateAppForm()
        return render(request, 'User/create-app.html', {"form": form})
    elif request.method == 'POST':
        form = CreateAppForm(request.POST)
        if form.is_valid():  # "Secret-Key": "fase-app:XOH3r_w74dxWVM9pwmEKaRsO-H4"
            app = form.save(commit=False)
            app_name = form.cleaned_data['app_name']
            secret_key = form.cleaned_data['app_secret_key']
            signer = Signer(secret_key)
            value = signer.sign(app_name)
            app.app_encrypted_key = value
            app.save()
            return Response({"Response": "Successfully Created App", "Secret Key": value},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({"Response": "An app already exists with this App Name or Secret Key"},
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def check_app_api(request):
    if request.method == 'POST':
        response = check_signature(request)
        if response is not None:
            return Response({"Response": "Success", "App": response}, status=status.HTTP_200_OK)
        else:
            return Response({"Response": "Tampered Signature"})


def check_signature(request):
    secret_key = request.META.get('HTTP_SECRET_KEY')
    encrypted_key = request.META.get('HTTP_ENCRYPTED_KEY')
    signer = Signer(secret_key)
    try:
        original = signer.unsign(encrypted_key)
        try:
            app = CreatedApps.objects.get(app_encrypted_key=encrypted_key)
            return AppSerializer(app).data
        except ObjectDoesNotExist:
            return None
    except BadSignature:
        return None


class UserRegistration(APIView):
    @staticmethod
    def post(request):
        response = check_signature(request)
        if response is not None:
            serializer = UserSerializer(data=request.data)
            # return Response({"User":serializer.data})
            if serializer.is_valid():
                serializer.save()
                user = User.objects.get(username=serializer.validated_data['username'])
                token = Token.objects.get(user=user)
                return Response({"Response": "Registration Successful", "Token": token.key},
                                status=status.HTTP_201_CREATED)
            else:
                return Response({"Success": "False"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Response": "Tampered Signature"})
