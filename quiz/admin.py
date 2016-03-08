from django.contrib import admin

from quiz.models import QuestionCategory, Question

@admin.register(QuestionCategory)
class CategoryAdmin(admin.ModelAdmin):
    pass
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass
