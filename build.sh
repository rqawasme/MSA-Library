#!/usr/bin/env bash
pip install -r requirements.txt
python3 manage.py migrate
# Fixtures removed — they were overwriting image_url and isbn on every deploy
# python3 manage.py loaddata superuser_fixture.json
# python3 manage.py loaddata books_fixture.json
python3 manage.py compilescss
python3 manage.py collectstatic
python3 manage.py findstatic pages/css/styles.css
# python3 manage.py crontab add