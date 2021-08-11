from django.shortcuts import render, redirect
from quiz.models import Test, Question, TestQuestion, Testrun, AnswerQuestion, TestrunStat
from quiz.forms import TestForm, CreateTestForm, CreateTestrunForm, CreateQuestionForm, SearchForm, FilterForm, LoginForm, RegisterForm
from django.views.generic import ListView, CreateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
import logging

logger = logging.getLogger(__name__)


class CreateTestView(LoginRequiredMixin, CreateView):
    login_url = '/login'

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
        content = request.POST.get('content')
        if len(content) > 1:
            q = Question(content=content)
            q.save()
            return redirect('/add')
        else:
            return render(request, 'create_question.html')


@method_decorator(cache_page(60 * 5), name='dispatch')
class TestListView(ListView):
    model = Test
    template_name = 'index.html'
    context_object_name = 'test_list'

    def get_queryset(self):
        return Test.objects.all()


class CreateTestrunView(LoginRequiredMixin, CreateView):
    current_testrun = 0
    login_url = '/login'

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
            test = context['test']
            tr = Testrun(test=test, user=self.request.user.username)
            tr.save()
            test.total_users += 1
            test.save()
            ts = TestrunStat(testrun=tr, test_name=context['test'].title)
            ts.save()
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
        global current_testrun
        test = context['test']
        answers = context['questions']
        tr = Testrun.objects.get(pk=current_testrun)
        ts = TestrunStat.objects.get(testrun=tr)
        ts.total_runs += 1
        is_full = True
        for q in answers:
            question = Question.objects.get(pk=q['id'])
            q_number = TestQuestion.objects.get(test=context['test'],
                                                question=question).number
            test_answer = AnswerQuestion.objects.get(testrun=tr,
                                                     question=question)
            str_answer = request.POST.get('answer_'+str(q_number))
            test_answer.answer = str_answer
            test_answer.save()
            if str_answer == "" and is_full:
                is_full = False
        if is_full:
            ts.full_answer += 1
        p = int((float(ts.full_answer)/float(ts.total_runs))*100)
        ts.percentage = p
        ts.save()
        return redirect('/')

    def get_queryset(self):
        return Testrun.objects.filter(test=self.request.resolver_match.kwargs['test_id'],
                                      user=self.request.user.username).order_by('-id')


class SearchTestView(CreateView):
    def get(self, request, **kwargs):
        form = SearchForm()
        return render(request, 'search.html')

    def post(self, request, **kwargs):
        form = SearchForm(request.POST)
        if form.is_valid():
            test = Test.objects.get(title=form.cleaned_data['title'])
            test_id = test.pk
            return redirect('/run_'+str(test_id))
        else:
            return render(request, 'search.html')


class FilterTestView(CreateView):
    def get(self, request, **kwargs):
        form = FilterForm()
        return render(request, 'filter.html')

    def post(self, request, **kwargs):
        form = FilterForm(request.POST)
        if form.is_valid():
            first = form.cleaned_data['first_date']
            second = form.cleaned_data['second_date']
            if form.cleaned_data['sorting'] == "asc":
                test_list = Test.objects.filter(created_at__gte=first).filter(created_at__lte=second).order_by(
                    'created_at')
            else:
                test_list = Test.objects.filter(created_at__gte=first).filter(created_at__lte=second).order_by(
                    '-created_at')
            context = {'test_list': test_list}
            return render(request, 'index.html', context=context)
        else:
            return render(request, 'filter.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None and user.is_active:
                login(request, user)
                return redirect('/')
        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/login')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'registration.html', {'form': form})
    else:
        form = RegisterForm()
    return render(request, 'registration.html', {'form': form})
