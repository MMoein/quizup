from django.contrib import admin

from quiz.models import QuestionCategory, Question

@admin.register(QuestionCategory)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name',]
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['text',]
