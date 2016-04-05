from django.db import models
import ast
import random
from Authentication.models import UserProfile


class ListField(models.TextField):
    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return unicode(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

class QuestionCategory(models.Model):
    name = models.CharField(verbose_name="name", max_length=100, default="")

    def __str__(self):
        return self.name


class Question(models.Model):
    text = models.TextField(verbose_name="Question")
    category = models.ForeignKey(QuestionCategory, verbose_name="Category")
    choice1 = models.CharField(max_length=255, verbose_name="Right answer")
    choice2 = models.CharField(max_length=255, verbose_name="Dummy answer1")
    choice3 = models.CharField(max_length=255, verbose_name="Dummy answer2")
    choice4 = models.CharField(max_length=255, verbose_name="Dummy answer3")


class Quiz(models.Model):
    category = models.ForeignKey(QuestionCategory, verbose_name="Category")

    competitor1 = models.ForeignKey(UserProfile, related_name='first_competitor')
    start_time1 = models.DateTimeField()
    score1 = models.IntegerField(blank=True, null=True)

    competitor2 = models.ForeignKey(UserProfile, related_name='second_competitor', null=True, blank=True)
    start_time2 = models.DateTimeField(blank=True, null=True)
    score2 = models.IntegerField(blank=True, null=True)
    questions = ListField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            q = Question.objects.filter(category=self.category).values_list('pk', flat=True)
            qlist = random.sample(range(0,len(q)) , 1)
            self.questions = []
            for pk in qlist:
                self.questions.append(q[pk])

        super(Quiz, self).save(*args, **kwargs)
    def __str__(self):
        return str(self.pk)