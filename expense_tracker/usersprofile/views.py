from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.contrib import messages

# Create your views here.


@never_cache
def profile(request, username):
             
    if request.user.is_authenticated and request.user.username == str(username):
            return render(
                 request, 
                 'usersprofile/profile.html', 
                 
                 {
                  'firstname': request.user.first_name, 
                  'lastname': request.user.last_name, 
                  'username': request.user.username, 
                  'email': request.user.email,
                 }

                )

    else:
        messages.error(request, 'You need authenticate first.')
        return redirect('users:signin')