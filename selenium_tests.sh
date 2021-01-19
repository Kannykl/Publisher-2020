#!/bin/bash

docker-compose down
execute_path="$0"

path=${execute_path/"/selenium_tests.sh"/""}

if [ "$OSTYPE" == "linux-gnu" ]
then
  if [ ! -e "$path/chromedriver" ]
  then
    echo "У вас нет драйвера, скачайте его и переместите в корень проекта"
  else
    python manage.py makemigrations publications_table
    python manage.py migrate
    python manage.py runserver &
    pytest publications_table/tests/selenium_tests.py
  fi
else
  if [ ! -e "$path/chromedriver.exe" ]
  then
    echo "У вас нет драйвера, скачайте его и переместите в корень проекта"
  else
    python manage.py makemigrations publications_table
    python manage.py migrate
    python manage.py runserver &
    pytest publications_table/tests/selenium_tests.py
  fi
fi
pkill -f runserver

sudo service postgresql stop