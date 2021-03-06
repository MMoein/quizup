# -*- coding: utf-8 -*-

import socket

from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.contrib.auth import authenticate, logout as l
from django.core.urlresolvers import reverse
from django.shortcuts import render
from .forms import *

import sha, random
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.contrib.auth import login as auth_login
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from quiz.functions import achievements

def signup(request):
    registered = False
    errors = []
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():

            user = User(**user_form.cleaned_data)
            user.username = user.email
            user.set_password(user.password)
            if User.objects.filter(email=user.email):
                errors = "already have this"
            else:
                user.save()
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.is_active = False
                salt = sha.new(str(random.random())).hexdigest()[:5]
                activation_key = sha.new(salt + user.username).hexdigest()
                profile.activation_key = activation_key
                # Now we save the UserProfile model instance.
                profile.save()
                s = "challenger.tk"
                activation_url = "http://"+str(s)+"/verify/" + activation_key
                send_mail('Activation link', activation_url , DEFAULT_FROM_EMAIL,
                        [user.email], fail_silently=False)
                registered = True
        else:
            errors = str(user_form.errors) + str(profile_form.errors)
            # return redirect(reverse('login'))
    elif request.method == 'GET':
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render_to_response('Authentication/signup.html',
                              {'user_form': user_form, 'profile_form': profile_form, 'registered': registered,
                               'error_message': errors},
                              context_instance=RequestContext(request))


def verify(request, token):
    userprofilelist = UserProfile.objects.filter(
        activation_key=token)
    if not userprofilelist:
        return HttpResponse("Error")
    userprofile = userprofilelist[0]
    userprofile.is_active = True
    userprofile.save()
    user = userprofile.user
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    auth_login(request, user)
    return HttpResponseRedirect('/')



def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    errors = []
    if request.method == 'POST':
        loginform = LoginForm(data=request.POST)
        if loginform.is_valid():
            username = loginform.cleaned_data['username']
            password = loginform.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                up = get_object_or_404(UserProfile, user=user)
                if up.is_active is True:
                    auth_login(request, user)
                    return redirect('/')
                else:
                    return render_to_response('Authentication/login.html',
                                              {'form': loginform,
                                               'error_message': u"ایمیل خود را تایید نکرده اید"},
                                              context_instance=RequestContext(request))
            else:
                return render_to_response('Authentication/login.html',
                                   {'form': loginform,
                                    'error_message': u"ایمیل نامعتبر است"},
                                   context_instance=RequestContext(request))
        else:
            errors = loginform.errors
    return render_to_response('Authentication/login.html',
                              {'form': LoginForm(), 'error_message': errors},
                              context_instance=RequestContext(request))


def profile(request):
    if not request.user.is_authenticated():
        return redirect(reverse('login'))
    achivs = achievements(request.user)
    errors = []
    if request.method == 'POST':

        user_form = UserForm(data=request.POST, instance=request.user)

        user_profile = UserProfile.objects.get(user=request.user)
        profile_form = UserProfileForm(data=request.POST, instance=user_profile)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():

            user_form.save()
            return render_to_response('Authentication/profile.html',
                                      {'user_form': user_form,
                                       'profile_form': profile_form,
                                       'messages': u'تغییرات اعمال شد',
                                       'error_message': errors,
                                       'achivements':achivs},
                                      context_instance=RequestContext(request))
        else:
            errors = str(user_form.errors) + str(profile_form.errors)
            # return redirect(reverse('profile))
            return render_to_response('Authentication/profile.html',
                                      {'user_form': user_form,
                                       'profile_form': profile_form,
                                       'error_message': errors,
                                       'achivements':achivs},
                                      context_instance=RequestContext(request))

    elif request.method == 'GET':
        user_profile = UserProfile.objects.get(user=request.user)
        user_form = UserForm(instance=request.user)
        user_profile_form = UserProfileForm(instance=user_profile)
        return render_to_response('Authentication/profile.html',
                                  {'user_form': user_form,
                                   'profile_form': user_profile_form,
                                   'error_message': errors,
                                   'achivements':achivs},
                                  context_instance=RequestContext(request))


def logout(request):
    l(request)
    return redirect(reverse('homepage'))
