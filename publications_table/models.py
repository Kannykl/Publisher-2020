"""Этот модуль содержит модель представления данных в бд."""
from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Author(models.Model):
    """Автор публикации."""
    name = models.CharField(max_length=255, verbose_name="имя")
    surname = models.CharField(max_length=255, unique=True, verbose_name="фамилия")
    patronymic = models.CharField(max_length=255, verbose_name="отчество")
    work_position = models.CharField(max_length=255, verbose_name="должность", blank=True)
    military_rank = models.CharField(max_length=255, verbose_name="звание", blank=True)

    objects = models.Manager()

    def __str__(self):
        return "" + self.initials()

    def initials(self):
        """ Получаем инициалы автора статей"""
        initials = self.surname + ' ' + self.name[:1] + '.' + self.patronymic[:1] + '.'
        return initials

    def __repr__(self):
        return self.surname

    class Meta:
        ordering = ('surname',)


class Type(models.Model):
    """Тип каждой статьи."""
    type_of_publication = models.CharField(max_length=255, verbose_name="тип публикации", null=True)
    enable = models.BooleanField(default=True)

    objects = models.Manager()

    def __str__(self):
        return self.type_of_publication

    def __repr__(self):
        return self.type_of_publication


class Publication(models.Model):
    """Публикация."""

    authors = models.ManyToManyField(Author, verbose_name="авторы", related_name='authors')
    title = models.CharField(max_length=256, verbose_name="название статьи")
    edition = models.CharField(max_length=255, verbose_name="издание", blank=True)
    type_of_publication = models.ForeignKey(Type, on_delete=models.DO_NOTHING, null=True)
    published_year = models.PositiveIntegerField(
        validators=[MaxValueValidator(datetime.now().year), MinValueValidator(1921)],
        verbose_name="год публикации", null=True, blank=True)
    range = models.CharField(max_length=255, verbose_name='диапазон', blank=True)
    uk_number = models.IntegerField(verbose_name='номер УК', null=True, blank=True, unique=True)
    is_selected = models.BooleanField(default=False, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title

    class Meta:
        """ По умолчанию записи на главной странице отсортированы по дате публикации,
         сначала - самые новые."""
        ordering = ('-published_year',)


class Table(models.Model):
    """Экспортируемые таблицы."""
    file = models.FileField(verbose_name='Таблица')
