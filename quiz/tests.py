from django.test import TestCase, Client
from quiz.models import Test, Question, TestQuestion, Testrun, AnswerQuestion
from django.forms.models import model_to_dict

class QuizTestCase(TestCase):

    def setUp(self):
        quiz = Test.objects.create(title='Test title',
                                   description='test')
        question_run1 = Question.objects.create(content='question 1')
        question_run2 = Question.objects.create(content='question 2')
        test_question1 = TestQuestion(test=quiz, question=question_run1, number=1)
        test_question2 = TestQuestion(test=quiz, question=question_run2, number=2)
        test_question1.save()
        test_question2.save()

    def tearDown(self):
        quiz = Test.objects.get(title='Test title')
        question_run1 = Question.objects.get(content='question 1')
        question_run2 = Question.objects.get(content='question 2')
        quiz.delete()
        question_run1.delete()
        question_run2.delete()

    def test_success_index(self):
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)

    def test_create_question(self):
        c = Client()
        c.post('/add_question', {'content': 'test question'})
        q = Question.objects.get(content='test question')
        q_id = q.pk
        self.assertEqual(model_to_dict(q), {'id': q_id, 'content': 'test question'})

    def test_create_test(self):
        c = Client()
        question1 = Question.objects.create(content='q 1')
        question2 = Question.objects.create(content='q 2')
        q1_id = str(question1.pk)
        q2_id = str(question2.pk)
        c.post('/add', {'title': 'test title', 'description': 'test description',
                                   'questions': (q1_id, q2_id)})
        t = Test.objects.get(title='test title')
        t_id = t.pk
        date = t.created_at
        self.assertEqual(model_to_dict(t), {'id': t_id, 'title': 'test title', 'description': 'test description',
                                            'created_at': date,
                                            'questions': [question1, question2]})

    def test_testrun(self):
        from pprint import pprint
        c = Client()
        t = Test.objects.get(title='Test title')
        path = '/run_'+str(t.pk)
        c.get(path)
        tr = Testrun.objects.get(test=t)
        c.post(path, {'answer_1': 'a 1', 'answer_2': 'a 2'})

        answers = list(AnswerQuestion.objects.filter(testrun=tr).values('question_content', 'answer'))
        self.assertEqual(answers, [{'question_content': 'question 1', 'answer': 'a 1'},
                                   {'question_content': 'question 2', 'answer': 'a 2'}])

