# -*- coding: utf-8 -*-
from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response, get_object_or_404

from django.template.context import RequestContext
from django.utils import timezone
from django.views.decorators.http import require_POST

from quiz.forms import QuestionForm, CategoryForm, ChallengeForm, InlineQuestionForm
from quiz.models import Question, Quiz, QuestionCategory
from Authentication.models import *
from .functions import make_challenge
import operator
from datetime import datetime

def home(request):
    return render_to_response('quiz/home.html', context_instance=RequestContext(request))

@require_POST
def search(request):
    search_query = request.POST['query']
    categories = QuestionCategory.objects.all()
    category = request.POST['cat_id'] if request.POST.has_key('cat_id') else None
    if category:
        questions = Question.objects.filter(text__contains=search_query, category__id=category)
    else:
        questions = Question.objects.filter(text__contains=search_query)
    return render_to_response('quiz/search.html', {'questions': questions, 'cats':categories, 'search':search_query}, context_instance=RequestContext(request))

def scoreboard(request):
    categories = QuestionCategory.objects.all()
    category = request.POST['cat_id'] if request.POST.has_key('cat_id') else None
    if category:
        quizs = Quiz.objects.filter(category__id=category)
        scores = {}
        for q in quizs:
            if q.competitor1 in scores:
                scores[q.competitor1] = scores[q.competitor1]+(q.score1 or 0)
            else:
                scores[q.competitor1] = (q.score1 or 0)

            if q.competitor2 in scores:
                scores[q.competitor2] = scores[q.competitor2]+(q.score2 or 0)
            else:
                scores[q.competitor2] = (q.score2 or 0)
        scores = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)[:5]
    else:
        scores = []
    print scores

    return render_to_response('quiz/scoreboard.html', {'cats':categories, 'scores':scores}, context_instance=RequestContext(request))


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
    quiz = Quiz.objects.get(pk=quiz_id)
    challenger = quiz.competitor1
    challengee = quiz.competitor2
    if request.user != challengee.user and request.user != challenger.user:
        raise Http404()

    if request.method == 'POST':
        points = 0
        question = Question.objects.get(pk=quiz.questions[quiz.answered_count1])
        # calculate points
        if request.POST.get('question', None) == question.choice1:
            if challenger.user == request.user:
                time_diff = (datetime.now(timezone.utc) - quiz.start_time1).seconds
                points = max(20 - time_diff, 0)
            else:
                time_diff = (datetime.now(timezone.utc) - quiz.start_time2).seconds
                points = max(20 - time_diff, 0)
        # update the quiz
        if challenger.user == request.user:
            quiz.answered_count1 += 1
            quiz.start_time1 = datetime.now(timezone.utc)
            quiz.score1 += points
            quiz.save()
        else:
            quiz.answered_count2 += 1
            quiz.start_time2 = datetime.now(timezone.utc)
            quiz.score2 += points
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
                               'form': f1},
                              context_instance=RequestContext(request))


def result(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render_to_response('quiz/result.html',
                              {'quiz': quiz, 'done1': quiz.answered_count1 >= len(quiz.questions), 'done2': quiz.answered_count2 >= len(quiz.questions)},
                              context_instance=RequestContext(request))


def make_quiz(request):
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
