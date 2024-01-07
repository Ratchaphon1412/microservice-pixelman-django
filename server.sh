#!/bin/bash

echo "-----------Apply migration--------- "
poetry run python3 manage.py makemigrations
poetry run python3 manage.py migrate
