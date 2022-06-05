from unittest.mock import DEFAULT
from django.db import models
from mcmen_dist_app.models import Property

class Brewer(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    nick_name = models.CharField(max_length=20)
    phone_num = models.CharField(max_length=15)

    def __str__(self):
        return self.nick_name
    
    class Meta:
        ordering = ('nick_name',)

class Brewery(models.Model):
    name = models.CharField(max_length=30)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    phone_num = models.CharField(max_length=15)
    brewers = models.ManyToManyField(Brewer)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)

class Kegs(models.Model):
    beer = models.CharField(max_length=30)
    brew_date = models.DateField()
    updated = models.DateField(null=True)
    category = models.CharField(max_length=20)
    brewery = models.ManyToManyField(Brewery)
    quantity = models.PositiveBigIntegerField()

    def __str__(self):
        return self.beer
    class Meta:
        ordering = ('beer',)
        verbose_name_plural= 'Kegs'

class Order(models.Model):
    beer = models.ForeignKey(Kegs, on_delete=models.PROTECT)
    quantity = models.PositiveBigIntegerField()
    property = models.ForeignKey(Property, on_delete=models.PROTECT)
    brewery = models.ForeignKey(
        Brewery, related_name='brewery', on_delete=models.PROTECT)
    manager = models.CharField(max_length=30)
    order_date = models.DateField()
    updated = models.DateField(null=True)
    status = models.CharField(max_length=10, default= 'Pending')

    def __str__(self):
        return f'•{self.beer} •{self.quantity} •{self.quantity}'
    
    class Meta:
        ordering = ('order_date',)
