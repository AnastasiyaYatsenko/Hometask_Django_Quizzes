from django.contrib import admin
import quiz.models


class TestQuestionsInline(admin.TabularInline):
    model = quiz.models.Test.questions.through


class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    inlines = [TestQuestionsInline]


class QuestionAdmin(admin.ModelAdmin):
    inlines = (TestQuestionsInline,)


admin.site.register(quiz.models.Test, TestAdmin)
admin.site.register(quiz.models.Question, QuestionAdmin)
