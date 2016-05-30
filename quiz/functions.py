import datetime
import socket

from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail

from .models import *

from django.db.models import Q

def make_challenge(challenger, challengee, category, _send_mail=True):
    quiz = Quiz(category=category, competitor1=challenger, start_time1=datetime.datetime.now(), competitor2=challengee)
    quiz.save()
    if _send_mail:
        #send email to challengee
        s = "challenger.tk"
        quiz_url = "http://"+str(s)+"/quiz/challenge/" + str(quiz.pk)
        send_mail('You have been challenged', quiz_url, DEFAULT_FROM_EMAIL,
                  [challengee.user.email], fail_silently=False)
    return quiz.pk

def achievements(user):
    userprofile = UserProfile.objects.get(user=user)
    quizs = Quiz.objects.filter(Q(competitor1=userprofile) | Q(competitor2=userprofile))
    achiv1 = len(quizs)>=3
    achiv2 = len(set(quizs.values_list('category',flat=True)))>2
    achiv3 = userprofile.time_in_quiz >= 1*60
    return [achiv1,achiv2,achiv3]