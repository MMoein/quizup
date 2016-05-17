# -*- coding: utf-8 -*-
import random

from django import forms

from quiz.models import Question, QuestionCategory
from Authentication.models import UserProfile


class QuestionForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=QuestionCategory.objects.all())

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['category'].label = u'دسته ی سوال'
        self.fields['text'].label = u'متن سوال'
        self.fields['choice1'].label = u'جواب درست'
        self.fields['choice2'].label = u'جواب غلظ'
        self.fields['choice3'].label = u'جواب غلظ'
        self.fields['choice4'].label = u'جواب غلظ'

    class Meta:
        model = Question
        fields = ('category', 'text', 'choice1', 'choice2', 'choice3', 'choice4')


class CategoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = u'نام دسته'

    class Meta:
        model = QuestionCategory
        fields = ('name',)


class ChallengeForm(forms.Form):
    category = forms.ModelChoiceField(queryset=QuestionCategory.objects.all())
    challengee = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(ChallengeForm, self).__init__(*args, **kwargs)
        self.fields['category'].label = u'دسته ی سوال'
        self.fields['challengee'].label = u'حریف'


class OnlineChallengeForm(forms.Form):
    category = forms.ModelChoiceField(queryset=QuestionCategory.objects.all())

    def __init__(self, *args, **kwargs):
        super(OnlineChallengeForm, self).__init__(*args, **kwargs)
        self.fields['category'].label = u'دسته ی سوال'


class InlineQuestionForm(forms.Form):

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super(InlineQuestionForm, self).__init__(*args, **kwargs)
        self.fields['question'] = forms.ChoiceField()
        self.fields['question'].widget = forms.RadioSelect()
        self.fields['question'].label = question.text
        choices = [(question.choice1, question.choice1), (question.choice2, question.choice2), (question.choice3, question.choice3), (question.choice4, question.choice4)]
        random.shuffle(choices)
        self.fields['question'].choices = choices
