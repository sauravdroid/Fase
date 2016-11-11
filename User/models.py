from django.db import models
from django.contrib.auth.models import User


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
    transaction_id = models.CharField(max_length=255,unique=True)
    data_string = models.TextField()