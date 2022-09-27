from django.db import models
from mcmen_dist_app.models import Property
from mcmen_user_app.models import UserProfile

class Brewery(models.Model):
    name = models.CharField(max_length=30)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    phone_num = models.CharField(max_length=15)
    brewers = models.ManyToManyField(UserProfile, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)

class Kegs(models.Model):
    beer = models.CharField(max_length=30)
    brew_date = models.DateField()
    updated = models.DateField(auto_now=True)
    sku = models.CharField(max_length=20)
    brewery = models.ManyToManyField(Brewery)
    quantity = models.PositiveBigIntegerField()

    def __str__(self):
        return self.beer
    class Meta:
        ordering = ('beer',)
        verbose_name_plural= 'Kegs'

class BrewLog(models.Model):
    author = models.CharField(max_length = 30)
    title = models.CharField(max_length = 20)
    text = models.TextField(max_length = 300)
    pub_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

class BrewLogComment(models.Model):
    post_connected = models.ForeignKey(
        BrewLog, related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length = 30)
    content = models.TextField(max_length = 300)
    date_posted = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.author) + ', ' + self.post_connected.title[:40]

class ComingSoon(models.Model):
    beer = models.CharField(max_length=30)
    sku = models.CharField(max_length=20)
    finish_date = models.DateField()
    description = models.CharField(max_length=75)
    brewery = models.ManyToManyField(Brewery)