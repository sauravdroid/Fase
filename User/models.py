from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.utils import timezone


class StockNew(models.Model):
    name = models.CharField(max_length=255)
    ticker = models.CharField(max_length=50)
    open = models.FloatField()
    close = models.FloatField()
    volume = models.IntegerField()

    def __str__(self):
        return self.name + ' ' + self.ticker


class CitrusResponse(models.Model):
    response_string = models.TextField()
    transaction_id = models.CharField(max_length=255, unique=True)
    data_string = models.TextField()

    def __str__(self):
        return self.transaction_id + " | " + self.response_string


class Seller(models.Model):
    seller = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    adress = models.TextField()
    city = models.CharField(max_length=255, default="none")
    state = models.CharField(max_length=255, default="none")
    phone_no = models.CharField(max_length=255, default="none", unique=True)
    pincode = models.IntegerField()

    def __str__(self):
        return self.seller.username


class FavoriteShop(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fseller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    tag = models.CharField(unique=True, max_length=510)

    def __str__(self):
        return self.tag + str(self.id)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class CreatedApps(models.Model):
    app_name = models.CharField(max_length=100, unique=True)
    app_secret_key = models.CharField(max_length=100, unique=True)
    app_encrypted_key = models.CharField(max_length=512, unique=True)
    created_at = models.DateTimeField(default=timezone.now())
    description = models.TextField(default="A simple android app for fase")

    def __str__(self):
        return self.app_name
