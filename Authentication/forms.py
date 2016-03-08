from Authentication.models import UserProfile
from django.contrib.auth.models import User
from django import forms
from captcha.fields import CaptchaField


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('sex', 'nationality')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())
    captcha = CaptchaField()