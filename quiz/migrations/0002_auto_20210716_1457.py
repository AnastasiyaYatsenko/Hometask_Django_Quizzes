# Generated by Django 3.2.5 on 2021-07-16 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='question',
        ),
        migrations.AlterField(
            model_name='testquestion',
            name='number',
            field=models.IntegerField(),
        ),
    ]
