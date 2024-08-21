from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import MyUser

# Create your views here.


def sign_up(request):

    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        username_is_busy = User.objects.filter(username = username).exists()
        user_exists = User.objects.filter(email = email).exists()

        if username_is_busy:
            messages.error(request, 'This Username is busy.')
            return redirect('users:signup')
        
        elif user_exists:
            messages.error(request, 'User with this Email address already registered.')
            return redirect('users:signup')     
           
        elif password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('users:signup')
        
        else:
            user = User.objects.create_user(
                first_name = firstname,
                last_name = lastname,
                username = username, 
                email = email,
                password = password1
            )
            myuser = MyUser(user = user, firstname = firstname, lastname = lastname)
            myuser.save()

            return redirect('users:signin')
    else:
        return render(request, 'users/signup.html', {})


def sign_in(request):
    
    return render(request, 'users/signin.html', {})


def forgot_pass(request):
    
    return render(request, 'users/forgotpass.html', {})


def reset_pass(request):
    
    return render(request, 'users/resetpass.html', {})


def profile(request):
    
    return render(request, 'users/profile.html', {})