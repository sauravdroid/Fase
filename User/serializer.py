from django.contrib.auth import get_user_model
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
        fields = ('first_name', 'last_name', 'username', 'email', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreatedApps
        fields = ('app_name', 'app_secret_key', 'app_encrypted_key')
