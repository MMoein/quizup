import datetime
import socket

from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail

from .models import *


def make_challenge(challenger, challengee, category):
    quiz = Quiz(category=category, competitor1=challenger, start_time1=datetime.datetime.now(), competitor2=challengee)
    quiz.save()
    #send email to challengee
    s = "challenger.tk"
    quiz_url = "http://"+str(s)+"/quiz/challenge/" + str(quiz.pk)
    send_mail('You have been challenged', quiz_url, DEFAULT_FROM_EMAIL,
              [challengee.user.email], fail_silently=False)
    return quiz.pk