#!/bin/bash

echo "----- Collect static files ------ " 
poetry run python3 manage.py collectstatic --noinput

echo "-----------Apply migration--------- "
poetry run python3 manage.py makemigrations
poetry run python3 manage.py migrate

echo "-----------Run gunicorn--------- "
poetry run gunicorn -b :80 auth.wsgi:application