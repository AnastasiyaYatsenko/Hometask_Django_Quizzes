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


class SearchForm(forms.Form):
    title = forms.CharField(min_length=5)


class FilterForm(forms.Form):
    first_date = forms.DateTimeField()
    second_date = forms.DateTimeField()
    sorting = forms.CharField()


class LoginForm(forms.Form):
    username = forms.CharField(max_length=120)
    password = forms.CharField(max_length=120,
                               widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=120)
    password = forms.CharField(max_length=120,
                               widget=forms.PasswordInput)
    confirm = forms.CharField(max_length=120,
                              widget=forms.PasswordInput)

    def clean(self):
        password = self.cleaned_data['password']
        confirm = self.cleaned_data['confirm']
        if password != confirm:
            raise forms.ValidationError('Passwords are not equal')
        return self.cleaned_data
