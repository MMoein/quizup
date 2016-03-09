from django.db import models


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