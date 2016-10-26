from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class FaseUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    path = models.CharField(max_length=500)

    def __str__(self):
        return self.user.get_full_name()


class FaseMerchant(models.Model):
    pass
