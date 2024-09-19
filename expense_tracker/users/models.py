from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User



class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    firstname = models.CharField(max_length = 25)
    lastname = models.CharField(max_length = 25)

    def __str__(self):
        return '{}'.format(self.user)
    
    def to_dict(self):
        return {
            'user': self.user.username,
            'firstname': self.firstname,
            'lastname': self.lastname,
        }

@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'firstname', 'lastname']
    search_fields = ['firstname', 'lastname']