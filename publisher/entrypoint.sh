#!/bin/sh

if [ "$DJANGO_DB_ENGINE" = "django.db.backends.postgresql" ]
then
    echo "Waiting for postgre..."

    while ! nc -z $DJANGO_DB_HOST $DJANGO_DB_PORT; do
      sleep 0.1
    done

    echo "DB started"
fi

python manage.py makemigrations publications_table
python manage.py migrate
python manage.py collectstatic --no-input --clear
export DJANGO_SETTINGS_MODULE="publisher.settings"
pytest -v

exec "$@"
