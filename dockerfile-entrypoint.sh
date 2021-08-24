#!/bin/sh
redis-server --daemonize yes
echo "Database migration"
python3 ./manage.py migrate
echo "Start celery worker"
celery -A django_quiz worker --loglevel=INFO --detach
echo "Start celery worker"
celery -A django_quiz beat --detach
echo "Start server"
python3 ./manage.py runserver 0.0.0.0:8000
