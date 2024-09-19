import ssl
import smtplib

from django.shortcuts import render, redirect

from email.message import EmailMessage

from .models import Message



def home(request):
    
    return render(request, 'home/index.html', {})


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

        return redirect('home:home')
    
    else:
        return render(request, 'home/contact.html', {})


def about(request):

    return render(request, 'home/about.html', {})