from django.db import models
from django.contrib.auth.models import User
from mcmen_dist_app.models import Property

class UserProfile(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_num = models.CharField(max_length=20)
    email = models.EmailField()
    job_title = models.CharField(max_length=20)
    home_base = models.ForeignKey(Property, on_delete=models.CASCADE)

    def __str__(self):
        return self.last_name + ', ' + self.first_name
    
    class Meta:
        ordering = ('last_name',)