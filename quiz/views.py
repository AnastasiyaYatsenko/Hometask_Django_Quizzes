from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Test
from django import forms


def index(request):
    context = {'quiz': Test.objects.all()}
    return render(request, 'quizzes/index.html', context=context)


def create_test(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            t = Test(title=(form.cleaned_data['title']), description=(form.cleaned_data['description']))
            t.save()
            return redirect('/quizzes')
        return render('quizzes/create_test.html', context={'form': form})
    return render(request, 'quizzes/create_test.html')


class TestForm(forms.Form):
    title = forms.CharField(min_length=5)
    description = forms.CharField(max_length=100)
