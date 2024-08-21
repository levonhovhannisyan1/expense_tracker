from django.contrib import admin
from .models import MyUser

# Register your models here.


class MyUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'firstname', 'lastname']
    search_fields = ['firstname', 'lastname']

admin.site.register(MyUser, MyUserAdmin)
