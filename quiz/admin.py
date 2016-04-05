from django.contrib import admin

from quiz.models import QuestionCategory, Question, Quiz

@admin.register(QuestionCategory)
class CategoryAdmin(admin.ModelAdmin):
    pass
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    fields = ['category', 'competitor1', 'start_time1', 'score1', 'competitor2', 'start_time2', 'score2', 'questions']