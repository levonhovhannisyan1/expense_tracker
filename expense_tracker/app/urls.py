from django.urls import path

from . import views



app_name = 'app'
urlpatterns = [
    path('', views.home, name = 'home'),
    path('contact-us/', views.contact, name = 'contact'),
    path('about-us/', views.about, name = 'about'),

    path('users/sign-up/', views.sign_up, name = 'signup'),
    path('users/sign-in/', views.sign_in, name = 'signin'),
    path('users/sign-out/', views.sign_out, name = 'signout'),
    path('users/forgot-password/', views.forgot_pass, name = 'forgotpass'),
    path('users/reset-password/', views.reset_pass, name = 'resetpass'),

    path('users/profile/<str:username>/', views.profile, name = 'profile'),
    path('users/profile/<str:username>/accounts/', views.accounts, name = 'accounts'),
    path('users/profile/<str:username>/dashboard/', views.dashboard, name = 'dashboard'),
    path('users/profile/<str:username>/report/', views.report, name = 'report'),
    path('users/profile/<str:username>/settings/', views.fsettings, name = 'settings'),
    path('users/profile/<str:username>/new-password', views.new_password, name = 'newpass'),
]