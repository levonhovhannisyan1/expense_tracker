from django.db import models
from django.contrib import admin



class Message(models.Model):
    name = models.CharField(max_length = 25)
    email = models.EmailField(max_length = 50)
    message = models.TextField()

    def __str__(self):
        return self.name
    
    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'message': self.message,
        }

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']
    search_fields = ['name', 'email']