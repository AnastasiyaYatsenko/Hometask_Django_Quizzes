# Generated by Django 3.2.5 on 2021-07-16 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_test_question'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='question',
        ),
    ]
