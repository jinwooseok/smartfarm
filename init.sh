#!/bin/bash

sleep 10  # PostgreSQL이 완전히 시작되길 기다림

python manage.py migrate
python manage.py loaddata initial_data.json

exec gunicorn -w 4 --env DJANGO_SETTINGS_MODULE=config.settings.prod config.wsgi:application --bind 0.0.0.0:8001 --timeout 300
