from django.db import models
from django.shortcuts import render


class Question(models.Model):
    content = models.CharField(max_length=255)

    def __str__(self):
        return self.content


class Test(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    questions = models.ManyToManyField('Question', through='TestQuestion')

    class Meta:
        ordering = [
         '-title']

    def __str__(self):
        return self.title


class TestQuestion(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    number = models.IntegerField()

    class Meta:
        ordering = [
         '-number']
