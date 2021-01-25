#!/bin/bash

docker-compose stop
pkill -f runserver

execute_path="$0"
project_path=${execute_path/"/selenium_tests.sh"/""}

read -p "Какой у вас браузер?(ответ=цифра) 1-Chrome 2-Mozilla  " browser


function install_driver_for_linux() {
  if [ "$browser" == "1" ]
  then
    wget https://chromedriver.storage.googleapis.com/88.0.4324.96/chromedriver_linux64.zip
    echo "chromedriver_linux64.zip"
  fi
  if [ "$browser" == "2" ]
    then
    wget https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-linux64.tar.gz
    echo "geckodriver-v0.29.0-linux64.tar.gz"
  fi
}


function steroid_script() {
  driver=$(install_driver_for_linux)
  if [ "$browser" == "2" ]
  then
    tar xzf "$driver"
    chmod +x "geckodriver"
  else
    unzip "$driver"
  fi
  rm "$driver"
  echo "К запуску тестов все готово ..."
}

function run_selenium() {
    python manage.py makemigrations publications_table
    python manage.py migrate
    python manage.py runserver &
    pytest publications_table/tests/selenium_tests.py
}


if [ "$OSTYPE" == "linux-gnu" ]
then
  if [ -e "$project_path/chromedriver" ] || [ -e "$project_path/geckodriver" ]
  then
    run_selenium
  else
    steroid_script
    run_selenium
  fi
fi
pkill -f runserver

sudo service postgresql stop