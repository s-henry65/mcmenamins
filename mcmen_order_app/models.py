from django.db import models
from mcmen_dist_app.models import Property
from mcmen_inventory_app.models import Brewery
from mcmen_inventory_app.models import Kegs
from django.contrib.auth.models import User


class OrderItem(models.Model):
    beer = models.ForeignKey(Kegs, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveBigIntegerField()
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True)
    brewery = models.ForeignKey(
        Brewery, related_name='brewery', on_delete=models.SET_NULL, null=True)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order_date = models.DateField()
    updated = models.DateField(auto_now=True)
    status = models.CharField(max_length=10, default='Pending')

    def __str__(self):
        return f'{self.property} •{self.brewery} •{self.order_date} •{self.beer} •{self.quantity}'

    class Meta:
        ordering = ('order_date',)


class Order(models.Model):
    order_items = models.ManyToManyField(OrderItem)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True)
    order_date = models.DateField()
    updated = models.DateField(auto_now=True)
    cart_status = models.CharField(max_length=10, default='Open')
    status = models.CharField(max_length=10, default='Pending')
    archive = models.BooleanField(default=False)
    notes = models.CharField(max_length=300, blank=True)
    keg_count = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f'{self.property} •{self.order_date} •{self.keg_count}'

    class Meta:
        ordering = ('order_date',)

