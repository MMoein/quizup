from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    sex = models.BooleanField()
    nationality = CountryField()
    is_active = models.BooleanField()
    activation_key = models.CharField(max_length=40)

    def __str__(self):
          return "%s's profile " % self.user