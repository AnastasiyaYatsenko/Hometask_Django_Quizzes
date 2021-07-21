from quiz.models import Test, Question, TestQuestion, Testrun, AnswerQuestion
from django import forms

class TestForm(forms.Form):
    title = forms.CharField(min_length=5)
    description = forms.CharField(max_length=100)


class CreateTestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'description', 'questions']
    title = forms.CharField()
    description = forms.TextInput()
    questions = forms.ModelMultipleChoiceField(
        queryset=Question.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )


class CreateTestrunForm(forms.ModelForm):
    class Meta:
        model = Testrun
        fields = ['test', 'answers']


class CreateQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['content']
    #content = forms.TextInput()
