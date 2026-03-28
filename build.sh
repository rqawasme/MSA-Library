#!/usr/bin/env bash
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata superuser_fixture.json
python manage.py loaddata books_fixture.json
python manage.py compilescss
python manage.py collectstatic
python manage.py findstatic pages/css/styles.css
# python manage.py crontab add