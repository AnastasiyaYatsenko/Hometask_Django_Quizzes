from django.db import models
from django.shortcuts import render
from datetime import datetime


class Question(models.Model):
    content = models.TextField(default="")

    def __str__(self):
        return self.content or ''


class Test(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    questions = models.ManyToManyField('Question', through='TestQuestion')
    created_at = models.DateTimeField(default=datetime.now())

    class Meta:
        ordering = [
         '-title']

    def __str__(self):
        return self.title or ''


class TestQuestion(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    number = models.IntegerField()

    class Meta:
        ordering = [
         '-number']


class Testrun(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    answers = models.ManyToManyField('Question', through='AnswerQuestion')

    class Meta:
        ordering = [
         '-test']


class AnswerQuestion(models.Model):
    testrun = models.ForeignKey(Testrun, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    question_content = models.TextField(default="")
    number = models.IntegerField()
    answer = models.TextField(default="")

    class Meta:
        ordering = [
         'number']


class TestrunStat(models.Model):
    testrun = models.ForeignKey(Testrun, on_delete=models.CASCADE)
    test_name = models.TextField(default="")
    full_answer = models.IntegerField(default=0)
    total_runs = models.IntegerField(default=0)
    percentage = models.IntegerField(default=0)

    class Meta:
        ordering = [
         'total_runs']
