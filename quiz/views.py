# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response

from django.template.context import RequestContext

from quiz.forms import QuestionForm, CategoryForm, ChallengeForm
from quiz.models import Question, Quiz, QuestionCategory
from Authentication.models import *
from .functions import make_challenge


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
    if request.user != challengee.user or request.user != challenger.user:
        raise Http404()
    return render_to_response('quiz/challenge.html',
                              {'quiz':quiz},
                              context_instance=RequestContext(request))

def make_quiz(request):
    if request.method == 'POST':
        challenge_form = ChallengeForm(data=request.POST)
        print challenge_form.errors
        if challenge_form.is_valid():
            cat = challenge_form.cleaned_data.get('category')
            challengee = challenge_form.cleaned_data.get('challengee')
            category = QuestionCategory.objects.get(name=cat)
            challengee_user = UserProfile.objects.get(user__email=challengee)
            challenger_user = UserProfile.objects.get(user=request.user)
            quiz_id = make_challenge(challenger_user, challengee_user, category)
            return HttpResponseRedirect('/quiz/challenge/' + str(quiz_id))
        else:
            raise Http404()

    else:
        return render_to_response('quiz/make-challenge.html',
                                  {'form':ChallengeForm()},
                                  context_instance=RequestContext(request))
