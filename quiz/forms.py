from django import forms

from quiz.models import Question, QuestionCategory


class QuestionForm(forms.ModelForm):
    category = forms.ModelChoiceField(label="Question Category",
                                      queryset=QuestionCategory.objects.all())

    class Meta:
        model = Question
        fields = ('category', 'text', 'choice1', 'choice2', 'choice3', 'choice4')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = QuestionCategory
        fields = ('name',)
