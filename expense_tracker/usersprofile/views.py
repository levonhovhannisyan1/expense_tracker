from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.contrib import messages

from .models import Profile



@never_cache
def profile(request, username):
             
    if request.user.is_authenticated and request.user.username == str(username):
            try:
                profile = Profile.objects.get(user=request.user)
            
            except Profile.DoesNotExist:
                 profile = None

            data = {
                'username': request.user.username,
                'firstname': request.user.first_name,
                'lastname': request.user.last_name,
                'profile': profile
            }
            return render(request, 'usersprofile/profile.html', data)

    else:
        messages.error(request, 'Authenticate first.')
        return redirect('users:signin')