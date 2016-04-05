# -*- coding: utf-8 -*-

from django import forms

from quiz.models import Question, QuestionCategory


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
