from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Stock(models.Model):
    name = models.CharField(max_length=255)
    ticker = models.CharField(max_length=50)
    open = models.FloatField()
    close = models.FloatField()
    volume = models.IntegerField()

    def __str__(self):
        return self.name + ' ' + self.ticker