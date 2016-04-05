# -*- coding: utf-8 -*-

from Authentication.models import UserProfile
from django.contrib.auth.models import User
from django import forms
from captcha.fields import CaptchaField


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = u'نام'
        self.fields['last_name'].label = u'نام‌خوانوادگی'
        self.fields['email'].label = u'ایمیل'
        self.fields['password'].label = u'رمز‌عبور'

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    radio_choices = [('MALE', u'مذکر'), ('FEMALE', u'مونث')]
    gender = forms.ChoiceField(label=u'جنسیت', choices=radio_choices, widget=forms.RadioSelect())

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['nationality'].label = u'ملیت'

    class Meta:
        model = UserProfile
        fields = ('gender', 'nationality')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, label='ایمیل')
    password = forms.CharField(widget=forms.PasswordInput(), label='رمز‌عبور')
    captcha = CaptchaField(label='')
