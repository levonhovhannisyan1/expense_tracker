from django.urls import path
from . import views


app_name = 'users'
urlpatterns = [
    path('sign-up/', views.sign_up, name = 'signup'),
    path('sign-in/', views.sign_in, name = 'signin'),
    path('forgot-password/', views.forgot_pass, name = 'forgotpass'),
    path('reset-password/', views.reset_pass, name = 'resetpass'),
    path('profile/', views.profile, name = 'profile'),
]