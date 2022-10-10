#!/usr/bin/env bash
pip install -r requirements.txt

python manage.py migrate
python manage.py loaddata superuser_fixture.json
# python manage.py collectstatic --clear
python manage.py collectstatic
python3 manage.py findstatic pages/css/styles.css
# python manage.py collectstatic --no-input
# python manage.py compilescss
# python manage.py compress --force