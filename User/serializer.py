from rest_framework import serializers
from .models import FavoriteShop
from .models import User
from .models import Seller

class SellerSeraialzer(serializers.ModelSerializer) :
    class Meta :
        model=Seller
        fields='__all__'

class FavoriteShopSerializer(serializers.ModelSerializer):
  class Meta :
       model=FavoriteShop
       #fields=('tag','seller','company_name','phone_no')
       fields = '__all__'
class UserSerializer(serializers.ModelSerializer):

    class Meta :
       model=User;
       fields='__all__'


