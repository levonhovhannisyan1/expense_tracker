from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.admin import SimpleListFilter

from django.utils import timezone
from datetime import timedelta



class Message(models.Model):
    name = models.CharField(max_length = 25)
    email = models.EmailField(max_length = 50)
    message = models.TextField()

    def __str__(self):
        return self.name

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']
    search_fields = ['name', 'email']



class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    firstname = models.CharField(max_length = 25)
    lastname = models.CharField(max_length = 25)

    def __str__(self):
        return '{}'.format(self.user)

@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'firstname', 'lastname']
    search_fields = ['firstname', 'lastname']



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    goal = models.IntegerField(null = True, blank = True, default = 0)
    limit = models.IntegerField(null = True, blank = True, default = 0)

    def __str__(self):
        return '{} {} {} {}'.format(self.user, self.avatar, self.goal, self.limit)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'avatar', 'goal', 'limit']
    search_fields = ['user']



class TypeFilter(SimpleListFilter):
    title = 'type'
    parameter_name = 'type'

    def lookups(self, request, model_admin):
        return (
            ('Income', 'Income'),
            ('Expense', 'Expense'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'Income':
            return queryset.filter(type=True)
        if self.value() == 'Expense':
            return queryset.filter(type=False)

class Account(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    amount = models.IntegerField()
    type = models.BooleanField()
    stable = models.BooleanField()
    category = models.CharField(max_length = 50)
    account_currency = models.CharField(max_length = 10, null = True, blank = True)
    action_date = models.DateField(auto_now_add = True, null=True, blank=True)

    def __str__(self):
        return '{} {} {} {} {} {} {}'.format(self.user, self.amount, self.type, self.stable, self.category, self.action_date, self.account_currency)

    def monthly_accounts(self):
        if self.action_date:
            current_date = timezone.now().date()

            one_month_later = self.action_date + timedelta(days=30)

            return current_date <= one_month_later
        return False

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'account_currency', 'custom_type_field_display', 'stable', 'category', 'action_date']
    search_fields = ['user__username', 'amount', 'stable', 'category']
    list_filter = ['user', TypeFilter, ('stable', admin.BooleanFieldListFilter), 'category']
    
    @admin.display(description='Type')
    def custom_type_field_display(self, obj):
        if obj.type:
            return 'Income'
        else:
            return 'Expense'