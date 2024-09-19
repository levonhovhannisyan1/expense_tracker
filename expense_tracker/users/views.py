import random
import ssl
import smtplib

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.contrib.auth.models import User

from email.message import EmailMessage

from .models import MyUser



@never_cache
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
        
        if user_exists:
            messages.error(request, 'User with this Email address already exists.')
            return redirect('users:signup')     
        
        elif username_is_busy:
            messages.error(request, 'This Username is busy.')
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

@never_cache
def sign_in(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username, password = password)
        
        if user is not None:

            if user.username == 'admin':
                login(request, user)
                return redirect('/admin/')
            
            else:
                login(request, user)
                return redirect(reverse('profile:profile', kwargs = {'username': username}))
        
        else:
            messages.error(request, 'Invalid Username or Password.')
            return redirect('users:signin')

    else:
        return render(request, 'users/signin.html', {})
    

def sign_out(request):

    logout(request)
    return redirect('users:signin')


def send_email_message_verification_code(request, email):

    code = random.randint(100000, 999999)
    request.session['code'] = code

    email_sender = 'levon.hovhannisyan1010@gmail.com'
    email_password = 'gscc dmzh ljxs thdf'
    email_receiver = '{}'.format(email)
    subject = 'Expense Tracker Password Reset Code'
    body = 'Your verification code is: {}\n\nDo not let anyone see this code!'.format(code)

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())


def forgot_pass(request):

    if request.method == 'POST':
        email = request.POST['email']
        request.session['email'] = email

        try: 
            User.objects.get(email = email)
            send_email_message_verification_code(request, email)

            request.session['access_reset_pass'] = True
            return redirect('users:resetpass')
        
        except User.DoesNotExist:
            messages.error(request, 'User does not exist.')
            return redirect('users:forgotpass')
    else:
        return render(request, 'users/forgotpass.html', {})


@never_cache
def reset_pass(request):

    if not request.session.get('access_reset_pass'):
        return redirect('users:forgotpass')

    email = request.session.get('email')
    code = request.session.get('code')

    if request.method =='POST':
        entered_code = request.POST['code']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']

        if entered_code == str(code):

            if pass1 == pass2:
                user = User.objects.get(email = email)
                user.set_password(pass1)
                user.save()

                request.session['access_reset_pass'] = None
                return redirect('users:signin')
                
            else:
                messages.error(request, 'Passwords do not match.')
                return redirect('users:resetpass')
                
        else:
            messages.error(request, 'Invalid Verification Code')
            return redirect('users:resetpass')
        
    return render(request, 'users/resetpass.html', {})
