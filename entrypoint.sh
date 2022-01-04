#!/usr/bin/env bash
python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py db_dump
python manage.py makesuperuser
python manage.py collectstatic --no-input --clear
gunicorn config.wsgi:application --bind 0.0.0.0:8000