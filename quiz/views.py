# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, render_to_response

# Create your views here.
from django.template.context import RequestContext

from quiz.forms import QuestionForm, CategoryForm
from quiz.models import Question


def home(request):
    return render_to_response('quiz/home.html', context_instance=RequestContext(request))


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
