from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, render_to_response

# Create your views here.
from django.template.context import RequestContext

from quiz.forms import QuestionForm, CategoryForm
from quiz.models import Question


def add_question(request):
    if not request.user.is_authenticated():
        return redirect(reverse('login'))

    registered = False
    errors = []

    if request.method == 'POST':
        question_form = QuestionForm(data=request.POST)
        # profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if question_form.is_valid():
            question_form.save()
            return render_to_response('quiz/add_success.html',
                                      {'error_message': question_form.errors},
                                      context_instance=RequestContext(request))
        else:
            return render_to_response('quiz/add_question.html',
                                      {'question_form': question_form, 'registered': registered,
                                       'error_message': question_form.errors},
                                      context_instance=RequestContext(request))
    elif request.method == 'GET':
        question_form = QuestionForm()
        # profile_form = UserProfileForm()
        return render_to_response('quiz/add_question.html',
                                  {'question_form': question_form, 'registered': registered, 'error_message': errors},
                                  context_instance=RequestContext(request))


def add_category(request):
    if not request.user.is_authenticated():
        return redirect(reverse('login'))

    registered = False
    errors = []
    if request.method == 'POST':
        category_form = CategoryForm(data=request.POST)
        # profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if category_form.is_valid():
            category_form.save()
            return render_to_response('quiz/add_success.html',
                                      {'error_message': category_form.errors},
                                      context_instance=RequestContext(request))
        else:
            return render_to_response('quiz/add_category.html',
                                      {'category_form': category_form, 'registered': registered,
                                       'error_message': category_form.errors},
                                      context_instance=RequestContext(request))
    elif request.method == 'GET':
        if not request.user.is_authenticated():
            return redirect(reverse('login'))
        category_form = CategoryForm
        # profile_form = UserProfileForm()
        return render_to_response('quiz/add_category.html',
                                  {'category_form': category_form, 'registered': registered, 'error_message': errors},
                                  context_instance=RequestContext(request))