import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_quiz.settings')

app = Celery('django_quiz')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'report-every-day': {
        'task': 'quiz.tasks.report',
        'schedule': crontab(minute='*/5'),#hour=20, minute=0),
    }
}
