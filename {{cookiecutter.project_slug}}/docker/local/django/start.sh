#!/bin/bash

set -o errexit
set -o nounset


python manage.py makemigrations --no-input
{% if cookiecutter.use_celery == 'y' and cookiecutter.use_beat == 'y' %}
python manage.py migrate django_celery_beat
{% endif %}
python manage.py migrate --no-input
python manage.py collectstatic --no-input

exec python manage.py runserver 0.0.0.0:8000