<h1>Этот репозиторий содержит код электронной библиотеки</h1>

<h2>Текущий функционал</h2>

- Создание записи в таблицу

- Удаление записи

- Редактирование записи

- Экспорт таблицы в Excel файл 

- Поиск записей по фамилии автора, названию статьи, изданию и номеру УК

- Фильтрация записей по типу публикации и году выпуска

- Сортировка по всем полям таблицы

  

<h3>В разработке применяется:</h3>

- Python 3.6.9
- Django 3

<h3>Установка</h3>

```
# Убедитесь, что активировано виртуальное окружение с python 3.6.9

git clone https://gitwork.ru/Kanny/publisher.git # копировать проект локально
pip install -r requirements.txt # установка зависимостей
python manage.py makemigrations publications_table # подготовка базы данных
python manage.py migrate # миграция (подготовка) базы данны
```

<h3>Запуск</h3>

```
python manage.py runserver # запуск проекта на http://127.0.0.1:8000/publisher/all_publications/
```

<h3>Docker</h3>

```
chmod +x entrypoint.sh # cделать файл entrypoint.sh исполняемым
docker-compose -f docker-compose.yml up --build
```

