from django.db import models


class QuestionCategory(models.Model):
    name = models.CharField(verbose_name="name", max_length=100, default="")

    def __str__(self):
        return self.name


class Question(models.Model):
    text = models.TextField(verbose_name="Question")
    category = models.ForeignKey(QuestionCategory, verbose_name="Category")