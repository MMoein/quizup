# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class UserProfile(models.Model):
    GENDER_CHOICES = [('M', 'MALE'), ('F', 'FEMALE')]

    user = models.OneToOneField(User)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    nationality = CountryField()
    is_active = models.BooleanField()
    activation_key = models.CharField(max_length=40)

    def __str__(self):
        return "%s's profile " % self.user
