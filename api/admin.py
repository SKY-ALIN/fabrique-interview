from django.contrib import admin

from .models import Pool, Question, AnswerOption

@admin.register(Pool)
class PoolAdmin(admin.ModelAdmin):
    list_display = ['title', 'start', 'end']
    search_fields = ['title']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'pool', 'type']
    search_fields = ['text', 'pool', 'type']


@admin.register(AnswerOption)
class AnswerOptionAdmin(admin.ModelAdmin):
    list_display = ['text', 'question']
    search_fields = ['text', 'question']
