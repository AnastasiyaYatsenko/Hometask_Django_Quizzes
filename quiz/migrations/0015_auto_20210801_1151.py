# Generated by Django 3.2.5 on 2021-08-01 11:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0014_auto_20210801_1027'),
    ]

    operations = [
        migrations.AddField(
            model_name='testrunstat',
            name='test_name',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='test',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 1, 11, 51, 19, 171360)),
        ),
    ]
