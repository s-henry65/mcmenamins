from unittest.mock import DEFAULT
from django.db import models
from mcmen_dist_app.models import Property
from django.contrib.auth.models import User


class Brewery(models.Model):
    name = models.CharField(max_length=30)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    phone_num = models.CharField(max_length=15)
    # brewers = models.ManyToManyField(Brewer)
    inv_view = models.CharField(max_length=10, default='Graphic')

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)

class Kegs(models.Model):
    beer = models.CharField(max_length=30)
    brew_date = models.DateField()
    updated = models.DateField(auto_now=True)
    category = models.CharField(max_length=20)
    brewery = models.ManyToManyField(Brewery)
    quantity = models.PositiveBigIntegerField()

    def __str__(self):
        return self.beer
    class Meta:
        ordering = ('beer',)
        verbose_name_plural= 'Kegs'

