import socket

from django.shortcuts import render
from .forms import *


import sha, random
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.mail import EmailMessage
from django.core.mail import send_mail


def signup(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():

            user = User(**user_form.cleaned_data)
            user.username = user.email
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.is_active = False
            salt = sha.new(str(random.random())).hexdigest()[:5]
            activation_key = sha.new(salt+user.username).hexdigest()
            profile.activation_key = activation_key
            # Now we save the UserProfile model instance.
            profile.save()
            s = socket.gethostbyname(socket.gethostname())
            activation_url = "http://"+str(s)+"/verify/" + activation_key
            send_mail('Activation link', activation_url , 'moein.zeraatkar@gmail.comf',
                    [user.email], fail_silently=False)
            registered = True
        else:
            print user_form.errors, profile_form.errors
    user_form = UserForm()
    profile_form = UserProfileForm()
    return render_to_response('Authentication/signup.html',
                              {'user_form':user_form, 'profile_form':profile_form, 'registered':registered},
                              context_instance=RequestContext(request))