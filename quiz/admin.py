from django.contrib import admin
from .models import QuizTheme, Question, Score

@admin.register(QuizTheme)
class QuizThemeAdmin(admin.ModelAdmin):
    list_display = ['nom', 'created_at']
    search_fields = ['nom', 'description']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['theme', 'type', 'question', 'created_at']
    list_filter = ['theme', 'type']
    search_fields = ['question']

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ['user', 'theme', 'points_total', 'date']
    list_filter = ['theme', 'date']
    search_fields = ['user__username']