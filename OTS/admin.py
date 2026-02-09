from django.contrib import admin

# Register your models here.

from .models import Candidate, Question, Result

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'test_attempted', 'points')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('qid', 'que', 'a', 'b', 'c', 'd', 'ans')
    list_filter = ('ans',)
    search_fields = ('que',)

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('resultid', 'username', 'date', 'attempt', 'right', 'wrong', 'points')
    list_filter = ('date',)
