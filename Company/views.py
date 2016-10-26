from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import Stock
from django.shortcuts import HttpResponse


# Create your views here.


# List all Stocks
# stocks/




class StockList(APIView):
    def get(self,request):
        stock = Stock.objects.all()
        serializer = StockSerializer(stock, many=True)
        return Response(serializer.data)

    def post(self):
        pass
