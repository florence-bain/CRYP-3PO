
web: gunicorn traderunner-cryp3po.wsgi:application --log-file - --log-level debug
python manage.py collectstatic --noinput
manage.py migrate