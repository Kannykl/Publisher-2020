#!/bin/bash

if [ "$DJANGO_DB_ENGINE" == "django.db.backends.postgresql_psycopg2" ]
then
    echo "Waiting for postgre..."

    while ! nc -z "$DJANGO_DB_HOST" "$DJANGO_DB_PORT"; do
      sleep 0.1
    done

    echo "DB started"
fi

python manage.py makemigrations publications_table
python manage.py migrate
python manage.py collectstatic --no-input --clear
export DJANGO_SETTINGS_MODULE="publisher.settings"

pytest publications_table/tests/test_views.py
pytest publications_table/tests/test_urls.py
pytest publications_table/tests/test_models.py

python manage.py runserver 0.0.0.0:8000

exec "$@"
