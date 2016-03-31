# -*- coding: utf-8 -*-

from Authentication.models import UserProfile
from django.contrib.auth.models import User
from django import forms
from captcha.fields import CaptchaField


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    radio_choices = [('MALE', 'MALE'), ('FEMALE', 'FEMALE')]
    gender = forms.ChoiceField(label=u'جنسیت', choices=radio_choices, widget=forms.RadioSelect())

    class Meta:
        model = UserProfile
        fields = ('gender', 'nationality')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())
    captcha = CaptchaField()
