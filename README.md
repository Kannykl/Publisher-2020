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


<h3>Docker</h3>

```
chmod +x entrypoint.sh # cделать файл entrypoint.sh исполняемым
docker-compose -f docker-compose.yml up --build
```

