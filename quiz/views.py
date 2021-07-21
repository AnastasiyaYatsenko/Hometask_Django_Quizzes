from django.http import HttpResponse
from django.shortcuts import render, redirect
from quiz.models import Test, Question, TestQuestion, Testrun, AnswerQuestion
from quiz.forms import TestForm, CreateTestForm, CreateTestrunForm, CreateQuestionForm
from django import forms
from django.forms import ValidationError
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from pprint import pprint


class CreateTestView(CreateView):
    def get(self, request, **kwargs):
        form = CreateTestForm()
        context = {
            'questions': Question.objects.all()
        }
        return render(request, 'create_test.html', context=context)

    def post(self, request, **kwargs):
        form = CreateTestForm(request.POST)
        if form.is_valid():
            t = Test(title=form.cleaned_data['title'],
                     description=form.cleaned_data['description'])
            t.save()
            i = 1
            for q in form.cleaned_data.get('questions'):
                test_question = TestQuestion(test=t, question=q, number=i)
                test_question.save()
                i += 1
            return redirect('/')
        else:
            context = {
                'form': form,
                'questions': Question.objects.all()
            }
            return render(request, 'create_test.html', context=context)


class CreateQuestionView(CreateView):
    def get(self, request, **kwargs):
        form = CreateQuestionForm()
        return render(request, 'create_question.html')

    def post(self, request, **kwargs):
        form = CreateQuestionForm()
        pprint(form.data)
        content = request.POST.get('content')
        if len(content) > 1:
            pprint(form.data)
            q = Question(content=content)
            q.save()
            return redirect('/add')
        else:
            return render(request, 'create_question.html')


class TestListView(ListView):
    model = Test
    template_name = 'index.html'
    context_object_name = 'test_list'

    def get_queryset(self):
        return Test.objects.all()


class CreateTestrunView(CreateView):
    current_testrun = 0

    def get_context_data(self, **kwargs):
        test_id = self.kwargs['test_id']
        test = Test.objects.get(pk=test_id)
        context = {
            'test': test,
            'questions': Question.objects.filter(test=test).values()
        }
        return context

    def get(self, request, **kwargs):
        form = CreateTestrunForm()
        context = self.get_context_data(**kwargs)
        test_queryset = self.get_queryset()
        is_retested = True
        if not test_queryset:
            tr = Testrun(test=context['test'])
            tr.save()
            is_retested = False
        else:
            tr = self.get_queryset()[0]
        global current_testrun
        current_testrun = tr.pk
        for q in context['questions']:
            question = Question.objects.get(pk=q['id'])
            q_number = TestQuestion.objects.get(test=context['test'],
                                                question=question).number
            if not is_retested:
                test_answer = AnswerQuestion(testrun=tr,
                                             question=question,
                                             question_content=question.content,
                                             number=q_number)
                test_answer.save()
        test_answers = AnswerQuestion.objects.filter(testrun=tr).values().order_by('number')
        context['answers'] = test_answers
        return render(request, 'run_test.html', context=context)

    def post(self, request, *args, **kwargs):
        form = CreateTestrunForm()
        context = self.get_context_data(**kwargs)
        pprint(form.data)
        global current_testrun
        test = context['test']
        answers = context['questions']
        tr = Testrun.objects.get(pk=current_testrun)
        for q in answers:
            question = Question.objects.get(pk=q['id'])
            q_number = TestQuestion.objects.get(test=context['test'],
                                                question=question).number
            test_answer = AnswerQuestion.objects.get(testrun=tr,
                                                     question=question)
            pprint(request.POST.get('answer_'+str(q_number)))
            test_answer.answer = request.POST.get('answer_'+str(q_number))
            test_answer.save()
        return redirect('/')

    def get_queryset(self):
        return Testrun.objects.filter(test=self.request.resolver_match.kwargs['test_id']).order_by('-id')
