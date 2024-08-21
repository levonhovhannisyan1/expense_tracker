from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    firstname = models.CharField(max_length = 25)
    lastname = models.CharField(max_length = 25)

    def __str__(self):
        return '{}'.format(self.user)