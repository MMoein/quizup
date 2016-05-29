# -*- coding: utf-8 -*-
from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response, get_object_or_404

from django.template.context import RequestContext
from django.utils import timezone
from django.views.decorators.http import require_POST

from quiz.forms import QuestionForm, CategoryForm, ChallengeForm, InlineQuestionForm, OnlineChallengeForm
from quiz.models import Question, Quiz, QuestionCategory, ChallengeRequest
from Authentication.models import *
from .functions import make_challenge
import operator
from datetime import datetime
import json
from django_countries.fields import CountryField
from django_countries.data import COUNTRIES
def home(request):
    return render_to_response('quiz/home.html', context_instance=RequestContext(request))

@require_POST
def search(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    search_query = request.POST['query']
    categories = QuestionCategory.objects.all()
    category = request.POST['cat_id'] if request.POST.has_key('cat_id') else None
    if category:
        questions = Question.objects.filter(text__contains=search_query, category__id=category)
    else:
        questions = Question.objects.filter(text__contains=search_query)
    return render_to_response('quiz/search.html', {'questions': questions, 'cats':categories, 'search':search_query}, context_instance=RequestContext(request))

def scoreboard(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    categories = QuestionCategory.objects.all()
    countries = COUNTRIES.items()
    country = request.POST['country'] if request.POST.has_key('country') else None
    category = request.POST['cat_id'] if request.POST.has_key('cat_id') else None
    selected_country = country.split('\'')[1] if country else None
    quizs = Quiz.objects.all()
    if category:
        quizs = quizs.filter(category__id=category)
    scores = {}
    for q in quizs:
        if q.competitor1.user.first_name in scores:
            scores[q.competitor1.user.first_name] = scores[q.competitor1.user.first_name]+(q.score1 or 0)
        else:
            if q.competitor1.nationality.code == selected_country or not selected_country:
                scores[q.competitor1.user.first_name] = (q.score1 or 0)

        if q.competitor2.user.first_name in scores:
            scores[q.competitor2.user.first_name] = scores[q.competitor2.user.first_name]+(q.score2 or 0)
        else:
            if q.competitor2.nationality.code == selected_country or not selected_country:
                scores[q.competitor2.user.first_name] = (q.score2 or 0)
    scores = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)[:5]
    return render_to_response('quiz/scoreboard.html', {'cats':categories, 'category':int(category) if category else category, 'countries':countries, 'selected_country':selected_country, 'scores':scores}, context_instance=RequestContext(request))


def add_question(request):
    if not request.user.is_authenticated():
        return redirect(reverse('login'))

    errors = []

    if request.method == 'POST':
        question_form = QuestionForm(data=request.POST)

        if question_form.is_valid():
            question_form.save()
            new_question_form = QuestionForm()
            return render_to_response('quiz/add_question.html',
                                      {'question_form': new_question_form,
                                       'messages': u'سوال جدید اضافه شد'},
                                      context_instance=RequestContext(request))
        else:
            return render_to_response('quiz/add_question.html',
                                      {'question_form': question_form,
                                       'error_message': question_form.errors},
                                      context_instance=RequestContext(request))
    elif request.method == 'GET':
        question_form = QuestionForm()
        return render_to_response('quiz/add_question.html',
                                  {'question_form': question_form, 'error_message': errors},
                                  context_instance=RequestContext(request))


def add_category(request):
    if not request.user.is_authenticated():
        return redirect(reverse('login'))

    errors = []
    if request.method == 'POST':
        category_form = CategoryForm(data=request.POST)

        if category_form.is_valid():
            category_form.save()
            new_category_form = CategoryForm()
            return render_to_response('quiz/add_category.html',
                                      {'category_form': new_category_form,
                                       'messages': u'دسته جدید اضافه شد',
                                       'error_message': category_form.errors},
                                      context_instance=RequestContext(request))
        else:
            return render_to_response('quiz/add_category.html',
                                      {'category_form': category_form,
                                       'error_message': category_form.errors},
                                      context_instance=RequestContext(request))
    elif request.method == 'GET':
        if not request.user.is_authenticated():
            return redirect(reverse('login'))
        category_form = CategoryForm
        return render_to_response('quiz/add_category.html',
                                  {'category_form': category_form,
                                   'error_message': errors},
                                  context_instance=RequestContext(request))


def challenge(request, quiz_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    quiz = Quiz.objects.get(pk=quiz_id)
    challenger = quiz.competitor1
    challengee = quiz.competitor2
    user_profile = UserProfile.objects.filter(user=request.user).first()
    if request.user != challengee.user and request.user != challenger.user:
        raise Http404()
    now_score = 0
    if request.method == 'POST':
        points = 0
        if quiz.competitor1 == user_profile:
            question = Question.objects.get(pk=quiz.questions[quiz.answered_count1])
            quiz.answerd1 = False
            quiz.valid1 = False
            quiz.save()
        elif quiz.competitor2 == user_profile:
            question = Question.objects.get(pk=quiz.questions[quiz.answered_count2])
            quiz.answerd2 = False
            quiz.valid2 = False
            quiz.save()
        else:
            raise Http404()
        # calculate points
        if request.POST.get('question', None) == question.choice1:
            if challenger.user == request.user:
                time = request.POST.get('timer', '0')
                if time == "":
                    time = '0'
                time_diff = int(time)
                challenger.time_in_quiz += time_diff
                challenger.save()
                points = max(20 - time_diff, 0)
            else:
                time = request.POST.get('timer', '0')
                if time == "":
                    time = '0'
                time_diff = int(time)
                challengee.time_in_quiz += time_diff
                challengee.save()
                points = max(20 - time_diff, 0)
        # update the quiz
        if challenger.user == request.user:
            quiz.answered_count1 += 1
            quiz.start_time1 = datetime.now(timezone.utc)
            quiz.score1 += points
            now_score = quiz.score1
            quiz.save()
        else:
            quiz.answered_count2 += 1
            quiz.start_time2 = datetime.now(timezone.utc)
            quiz.score2 += points
            now_score = quiz.score2
            quiz.save()

    if challenger.user == request.user:
        if quiz.answered_count1 == 0:
            quiz.start_time1 = datetime.now(timezone.utc)
            quiz.save()

        if quiz.answered_count1 >= len(quiz.questions):
            return redirect(reverse('result', kwargs={'quiz_id': quiz_id}))

        question_id = quiz.questions[quiz.answered_count1]
        question = Question.objects.get(id=question_id)
        f1 = InlineQuestionForm(question=question)
    else:
        if quiz.answered_count2 == 0:
            quiz.start_time2 = datetime.now(timezone.utc)
            quiz.save()

        if quiz.answered_count2 >= len(quiz.questions):
            result_link = "http://" + "challenger.tk" + "/result/" + str(quiz_id)
            send_mail('Challenge result', result_link, DEFAULT_FROM_EMAIL,
                      [challenger.user.email, challengee.user.email], fail_silently=False)
            return redirect(reverse('result', kwargs={'quiz_id': quiz_id}))

        question_id = quiz.questions[quiz.answered_count2]
        question = Question.objects.get(id=question_id)
        f1 = InlineQuestionForm(question=question)
    return render_to_response('quiz/challenge.html',
                              {'quiz': quiz,
                               'form': f1,
                               'score': now_score},
                              context_instance=RequestContext(request))


def select(request, quiz_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    quiz = Quiz.objects.get(pk=quiz_id)
    challenger = quiz.competitor1
    challengee = quiz.competitor2

    user_profile = UserProfile.objects.filter(user=request.user).first()
    if request.user != challengee.user and request.user != challenger.user:
        raise Http404()
    if request.method == 'POST':
        if quiz.competitor1 == user_profile:
            quiz.answerd1 = True
            question = Question.objects.get(pk=quiz.questions[quiz.answered_count1])
            if request.POST.get('question', None) == question.choice1:
                quiz.valid1 = True
            else:
                quiz.valid1 = False

        elif quiz.competitor2 == user_profile:
            quiz.answerd2 = True
            question = Question.objects.get(pk=quiz.questions[quiz.answered_count2])
            if request.POST.get('question', None) == question.choice1:
                quiz.valid2 = True
            else:
                quiz.valid2 = False
        else:
            raise Http404()
    quiz.save()
    return HttpResponse("")


def result(request, quiz_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render_to_response('quiz/result.html',
                              {'quiz': quiz, 'done1': quiz.answered_count1 >= len(quiz.questions), 'done2': quiz.answered_count2 >= len(quiz.questions)},
                              context_instance=RequestContext(request))


def make_quiz(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    if request.method == 'POST':
        challenge_form = ChallengeForm(data=request.POST)
        if challenge_form.is_valid():
            cat = challenge_form.cleaned_data.get('category')
            challengee = challenge_form.cleaned_data.get('challengee')
            category = QuestionCategory.objects.get(name=cat)
            challengee_user = UserProfile.objects.filter(user__email=challengee).first()
            challenger_user = UserProfile.objects.filter(user=request.user).first()
            if challenger_user is None or challengee_user is None or challengee_user == challenger_user:
                return render_to_response('quiz/make-challenge.html',
                                          {'form': ChallengeForm(),
                                           'messages': u'لطفا یک کاربر دیگر انتخاب کنید'},
                                          context_instance=RequestContext(request))

            quiz_id = make_challenge(challenger_user, challengee_user, category)
            return HttpResponseRedirect('/quiz/challenge/' + str(quiz_id))
        else:
            raise Http404()

    else:
        return render_to_response('quiz/make-challenge.html',
                                  {'form': ChallengeForm()},
                                  context_instance=RequestContext(request))


def online_challenge(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    if request.method == 'POST':
        challenge_form = OnlineChallengeForm(data=request.POST)
        if challenge_form.is_valid():
            category_id = challenge_form.cleaned_data.get('category')
            category = QuestionCategory.objects.get(name=category_id)
            challege_req = ChallengeRequest.objects.exclude(user=request.user).filter(category=category).first()
            if challege_req is not None:
                opponent = challege_req.user
                challengee_user = UserProfile.objects.filter(user=opponent).first()
                challenger_user = UserProfile.objects.filter(user=request.user).first()
                challege_req.delete()
                quiz_id = make_challenge(challenger_user, challengee_user, category, _send_mail=False)
                return HttpResponseRedirect('/quiz/challenge/' + str(quiz_id))

            ChallengeRequest.objects.get_or_create(user=request.user, category=category)
            return render_to_response('quiz/wait.html', {}, context_instance=RequestContext(request))

        else:
            return render_to_response('quiz/online-challenge.html',
                                      {'category_form': challenge_form,
                                       'error_message': challenge_form.errors},
                                      context_instance=RequestContext(request))
    else:
        return render_to_response('quiz/online-challenge.html',
                                  {'form': OnlineChallengeForm()},
                                  context_instance=RequestContext(request))


def challenge_search(request):
    challenger_user = UserProfile.objects.filter(user=request.user).first()
    quiz = Quiz.objects.filter(competitor2=challenger_user, start_time2__isnull=True).first()
    if quiz is not None:
        return HttpResponse('/quiz/challenge/' + str(quiz.id))
    return HttpResponse('-1')


def stats(request, quiz_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    quiz = Quiz.objects.get(id=quiz_id)
    user_profile = UserProfile.objects.filter(user=request.user).first()
    if user_profile is None or (not quiz.competitor1 == user_profile and not quiz.competitor2 == user_profile):
        raise Http404()
    score = quiz.score1 if quiz.competitor1 == user_profile else quiz.score2
    mycount = quiz.answered_count1 if quiz.competitor1 == user_profile else quiz.answered_count2
    opponent_score = quiz.score2 if quiz.competitor1 == user_profile else quiz.score1
    opponent_count = quiz.answered_count2 if quiz.competitor1 == user_profile else quiz.answered_count1
    answered = quiz.answerd2 if quiz.competitor1 == user_profile else quiz.answerd1
    valid = quiz.valid2 if quiz.competitor1 == user_profile else quiz.valid1
    return HttpResponse(
        json.dumps({'self_score': score, 'opponent_score': opponent_score, 'valid': valid, 'answered': answered,
        'mycount': mycount, 'opponent_count': opponent_count}))
