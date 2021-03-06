# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class UserProfile(models.Model):
    GENDER_CHOICES = [('MALE', 'MALE'), ('FEMALE', 'FEMALE')]

    user = models.OneToOneField(User)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    nationality = CountryField()
    is_active = models.BooleanField()
    activation_key = models.CharField(max_length=40)
    time_in_quiz = models.IntegerField(default=0)
    def __str__(self):
        return "%s's profile " % self.user
