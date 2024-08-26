from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.contrib import messages

# Create your views here.


@never_cache
def profile(request, username):
             
    if request.user.is_authenticated and request.user.username == username:
            return render(request, 'usersprofile/profile.html', {'username': username})

    else:
        messages.error(request, 'You need authenticate first.')
        return redirect('users:signin')