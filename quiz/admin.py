from django.contrib import admin
import quiz.models


class TestQuestionsInline(admin.TabularInline):
    model = quiz.models.Test.questions.through


class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    inlines = [TestQuestionsInline]


class QuestionAdmin(admin.ModelAdmin):
    inlines = (TestQuestionsInline,)


class TestAnswersInline(admin.TabularInline):
    model = quiz.models.Testrun.answers.through


class TestrunAdmin(admin.ModelAdmin):
    inlines = [TestAnswersInline]


admin.site.register(quiz.models.Test, TestAdmin)
admin.site.register(quiz.models.Question, QuestionAdmin)
admin.site.register(quiz.models.Testrun, TestrunAdmin)
