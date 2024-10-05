import os
import random
import ssl
import smtplib
import matplotlib.pyplot as plt
import requests

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.conf import settings
from django.db.models import Sum
from django.contrib.auth.models import User

from email.message import EmailMessage
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

from matplotlib.ticker import FuncFormatter

from .models import MyUser, Message, Profile, Account



url = "https://www.rate.am/hy/armenian-dram-exchange-rates/banks"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

prices = soup.find_all("div", class_="relative flex z-1 items-center h-full")

prices_list = []

for price in prices:
    prices_list.append(price)

prices_list = prices_list[0::3]

dollar_price = int(prices_list[8].text)



def home(request):
    return render(request, 'app/index.html', {})


def receive_email_message_from_customer(name, email, message_content):

    email_sender = 'levon.hovhannisyan1010@gmail.com'
    email_password = 'gscc dmzh ljxs thdf'
    email_receiver = 'levon.hovhannisyan2020@gmail.com'
    subject = 'Message From Customer'
    body = 'From:\n{}   -   {}\n\nThe message: {}'.format(name, email, message_content)

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())


def send_email_message_to_customer(name, email):

    email_sender = 'levon.hovhannisyan1010@gmail.com'
    email_password = 'gscc dmzh ljxs thdf'
    email_receiver = '{}'.format(email)
    subject = 'Expense Tracker FeedBack'
    body = 'Dear {}\nWe appreciate your criticism, thank you for your message, our specialists will contact you soon.\n\nWith love Expense Tracker'.format(name)

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())


def contact(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message_content = request.POST.get('message')

        message = Message(name = name, email = email, message = message_content)
        message.save()
        receive_email_message_from_customer(name, email, message_content)
        send_email_message_to_customer(name, email)
        return redirect('app:home')
    
    else:
        return render(request, 'app/contact.html', {})

def about(request):
    return render(request, 'app/about.html', {})


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
            return redirect('app:signup')     
        
        elif username_is_busy:
            messages.error(request, 'This Username is busy.')
            return redirect('app:signup')
           
        elif password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('app:signup')
        
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
            return redirect('app:signin')
        
    else:
        return render(request, 'app/signup.html', {})


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
                return redirect(reverse('app:profile', kwargs = {'username': username}))
        
        else:
            messages.error(request, 'Invalid Username or Password.')
            return redirect('app:signin')

    else:
        return render(request, 'app/signin.html', {})
    

def sign_out(request):

    logout(request)
    return redirect('app:signin')


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
            return redirect('app:resetpass')
        
        except User.DoesNotExist:
            messages.error(request, 'User does not exist.')
            return redirect('app:forgotpass')
    else:
        return render(request, 'app/forgotpass.html', {})


@never_cache
def reset_pass(request):

    if not request.session.get('access_reset_pass'):
        return redirect('app:forgotpass')

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
                return redirect('app:signin')
                
            else:
                messages.error(request, 'Passwords do not match.')
                return redirect('app:resetpass')
                
        else:
            messages.error(request, 'Invalid Verification Code')
            return redirect('app:resetpass')
        
    return render(request, 'app/resetpass.html', {})


def get_user_balance_per_day(username):

    today = datetime.today()
    days_in_month = (today.replace(month=today.month % 12 + 1, day=1) - timedelta(days=1)).day  # Get number of days in current month
    
    balances = []

    for day in range(1, days_in_month + 1):
        year = today.year
        month = today.month

        total_amd_incomes = Account.objects.filter(
            user__username=username, type=True, account_currency='AMD', 
            action_date__year=year, action_date__month=month, action_date__day=day
        ).aggregate(total_income=Sum('amount'))['total_income'] or 0

        total_amd_expenses = Account.objects.filter(
            user__username=username, type=False, account_currency='AMD', 
            action_date__year=year, action_date__month=month, action_date__day=day
        ).aggregate(total_expense=Sum('amount'))['total_expense'] or 0

        total_usd_incomes = Account.objects.filter(
            user__username=username, type=True, account_currency='USD', 
            action_date__year=year, action_date__month=month, action_date__day=day
        ).aggregate(total_income=Sum('amount'))['total_income'] or 0

        total_usd_expenses = Account.objects.filter(
            user__username=username, type=False, account_currency='USD', 
            action_date__year=year, action_date__month=month, action_date__day=day
        ).aggregate(total_expense=Sum('amount'))['total_expense'] or 0

        total_income_usd = (total_amd_incomes / dollar_price) + total_usd_incomes
        total_expense_usd = (total_amd_expenses / dollar_price) + total_usd_expenses

        daily_balance = total_income_usd - total_expense_usd

        balances.append(daily_balance)

    days_of_month = list(range(1, days_in_month + 1))

    return days_of_month, balances

def make_a_graph(username):
    days_of_month, balances = get_user_balance_per_day(username)

    plt.figure(figsize=(10, 5))
    plt.plot(days_of_month, balances, marker='o')
    
    plt.title(f'Balance Over Days for {username}')
    plt.xlabel('Day of the Month')
    plt.ylabel('Balance (USD)')
    
    def format_func(value, tick_number):
        return f'{int(value):,}'
    
    plt.gca().yaxis.set_major_formatter(FuncFormatter(format_func))
    plt.xticks(days_of_month)
    plt.grid()
    
    graph_filename = f'graph_{username}.png'
    graph_directory = os.path.join(settings.BASE_DIR, 'static', 'graphs')

    if not os.path.exists(graph_directory):
        os.makedirs(graph_directory)
    
    img_path = os.path.join(graph_directory, graph_filename)
    plt.savefig(img_path)
    plt.close()

    return f'graphs/{graph_filename}'

@never_cache
def profile(request, username):

    if request.method == 'GET':
    
        if request.user.is_authenticated and request.user.username == str(username):
            try:
                profile = Profile.objects.get(user=request.user)
            except Profile.DoesNotExist:
                profile = None

            info = {
                'username': request.user.username,
                'firstname': request.user.first_name,
                'lastname': request.user.last_name,
                'profile': profile,
            }

            amd_incomes_sum = Account.objects.filter(
                user__username=username,
                type=True,
                account_currency='AMD'
            ).aggregate(total=Sum('amount'))['total'] or 0

            amd_expenses_sum = Account.objects.filter(
                user__username=username,
                type=False,
                account_currency='AMD'
            ).aggregate(total=Sum('amount'))['total'] or 0

            usd_incomes_sum = Account.objects.filter(
                user__username=username,
                type=True,
                account_currency='USD'
            ).aggregate(total=Sum('amount'))['total'] or 0

            usd_expenses_sum = Account.objects.filter(
                user__username=username,
                type=False,
                account_currency='USD'
            ).aggregate(total=Sum('amount'))['total'] or 0

            total_incomes_usd = (amd_incomes_sum / dollar_price) + usd_incomes_sum
            total_expenses_usd = (amd_expenses_sum / dollar_price) + usd_expenses_sum

            usd_balance = total_incomes_usd - total_expenses_usd
            usd_spent = total_expenses_usd

            latest_accounts = Account.objects.filter(user__username=username, stable=False).order_by('-id')[:5]

            graph_image_path = make_a_graph(username)

            data = {
                'info': info, 
                'latest_accounts': latest_accounts,    
                'usd_balance': int(usd_balance),
                'usd_spent': int(usd_spent),
                'graph_image': graph_image_path,
            }

            if latest_accounts:
                return render(request, 'app/profile.html', data)
            else:
                messages.error(request, 'There are no Accounts yet.')
                return render(request, 'app/profile.html', data)

        else:
            messages.error(request, 'Authenticate first.')
            return redirect('app:signin')
    
    else:
        return render(request, 'app/profile.html', {'username': username})

    
@never_cache
def accounts(request, username):

    if request.user.is_authenticated and request.user.username == str(username):
        accounts = Account.objects.filter(user__username = username)
        
        try:
            profile = Profile.objects.get(user=request.user)

        except Profile.DoesNotExist:
            profile = None

        info = {
            'username': request.user.username,
            'firstname': request.user.first_name,
            'lastname': request.user.last_name,
            'profile': profile,
        }

        if accounts.exists():
            accounts_list = []

            for account in accounts:

                if account.monthly_accounts():
                    accounts_list.append(account)

            if accounts_list:
                return render(request, 'app/accounts.html', {'info': info, 'accounts': accounts_list})
            
            else:
                messages.error(request, 'No monthly Accounts yet.')
                return render(request, 'app/accounts.html', {'username': username})
                
        else:
            messages.error(request, 'No monthly Accounts yet.')
            return render(request, 'app/accounts.html', {'username': username})

    else:
        messages.error(request, 'Authenticate first.')
        return redirect('app:signin')


@never_cache
def dashboard(request, username):

    if request.user.is_authenticated and request.user.username == str(username):

        if request.method == 'POST':
            amount = request.POST.get('amount', None)
            stability = request.POST.get('stability', None)
            type = request.POST.get('type', None)
            category = request.POST.get('category', None)
            other_category = request.POST.get('other-category', None)
            account_currency = request.POST.get('account-currency', None)
            goal = request.POST.get('goal', 0)
            limit = request.POST.get('limit', 0)

            try:
                usr_profile = Profile.objects.get(user = request.user)
                
            except Profile.DoesNotExist:
                usr_profile = Profile(user = request.user)
                usr_profile.save()

            if amount != None and stability != None and type != None and category != None:

                if stability == 'True':
                    stability = True
                
                elif stability == 'False':
                    stability = False

                if type == 'True':
                    type = True
                
                elif type == 'False':
                    type = False

                if category == 'Other':
                    final_category = other_category

                else:
                    final_category = category

                account = Account(user = request.user, amount = amount, type = type, stable = stability, category = final_category, account_currency = account_currency)
                account.save()
            
            elif goal != '':
                usr_profile.goal = goal
                usr_profile.save()

            elif limit != '':
                usr_profile.limit = limit
                usr_profile.save()

            return redirect(reverse('app:profile', args=[request.user.username]))

        else:
            return render(request, 'app/dashboard.html', {'username': username})

    else:
        messages.error(request, 'Authenticate first.')
        return redirect('app:signin')


@never_cache
def report(request, username):
    return render(request, 'app/report.html', {'username': username})


@never_cache
def fsettings(request, username):

    if request.user.is_authenticated and request.user.username == str(username):

        if request.method == 'POST':
            avatar = request.FILES.get('avatar', None)
            user_name = request.POST.get('username', None)
            firstname = request.POST.get('firstname', None)
            lastname = request.POST.get('lastname', None)
            email = request.POST.get('email', None)

            try:
                usr_profile = Profile.objects.get(user = request.user)
            
            except Profile.DoesNotExist:
                usr_profile = Profile(user = request.user)
                usr_profile.save()

            user = User.objects.get(username = request.user.username)
            myuser = MyUser.objects.get(user = request.user)

            if avatar:
                usr_profile.avatar = avatar
                usr_profile.save()

            if user_name:
                user.username = user_name
                user.save()
                login(request, user)
                return redirect(reverse('app:profile', kwargs = {'username': user_name}))
            
            if firstname:
                user.first_name = firstname
                myuser.firstname = firstname
                user.save()
                myuser.save()

            if lastname:
                user.last_name = lastname
                myuser.lastname = lastname
                user.save()
                myuser.save()

            if email:
                user.email = email
                user.save()

            return profile(request, username)

        else:
            return render(request, 'app/settings.html', {'username': username})

    else:
        messages.error(request, 'Authenticate first.')
        return redirect('app:signin')


@never_cache
def new_password(request, username):

    if request.user.is_authenticated and request.user.username == str(username):

        if request.method == 'POST':
            oldpass = request.POST['oldpass']
            new_password = request.POST['password1']
            confirmed_password = request.POST['password2']

            user = authenticate(request, username=username, password=oldpass)

            if user is not None:

                if new_password == confirmed_password:
                    user.set_password(new_password)
                    user.save()
                    return redirect('app:signin')

                else:
                    messages.error(request, 'Passwords do not match.')
                    return redirect('app:newpass', username=request.user.username)
        
            else:
                messages.error(request, 'Wrong Password.')
                return redirect('app:newpass', username=request.user.username)

        else:
            return render(request, 'app/newpass.html', {'username': username})

    else:
        messages.error(request, 'Authenticate first.')
        return redirect('app:signin')
