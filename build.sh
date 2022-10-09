#!/usr/bin/env bash
pip install -r requirements.txt

python manage.py migrate
python manage.py collectstatic --no-input
# python manage.py compilescss
python manage.py compress --force