from rest_framework import serializers
from .models import FavoriteShop, User, Seller, CreatedApps


class SellerSeraialzer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'


class FavoriteShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteShop
        # fields=('tag','seller','company_name','phone_no')
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreatedApps
        fields = ('app_name', 'app_secret_key','app_encrypted_key')
