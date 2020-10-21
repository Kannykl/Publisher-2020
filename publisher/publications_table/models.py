from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime


class Author(models.Model):
    """Автор публикации"""
    name = models.CharField(max_length=255, null=False, verbose_name="имя")
    surname = models.CharField(max_length=255, null=False, unique=True, verbose_name="фамилия")
    patronymic = models.CharField(max_length=255, null=False, verbose_name="отчество")
    work_position = models.CharField(max_length=255, null=False, verbose_name="должность")
    military_rank = models.CharField(max_length=255, null=False, verbose_name="звание")

    def __str__(self):
        return "" + self.get_initials()

    def get_initials(self):
        """ Получаем инициалы автора статей"""
        initials = self.surname + ' ' + self.name[:1] + '.' + self.patronymic[:1] + '.'
        return initials

    def __repr__(self):
        return self.surname

    class Meta:
        ordering = ('surname',)


class Publication(models.Model):
    """Запись в таблице о публикации"""

    TYPES_OF_PUBLICATIONS = (
        ('Тезис', 'Тезис'),
        ('Статья', 'Статья',)
    )

    authors = models.ManyToManyField(Author, verbose_name="авторы")
    title = models.CharField(max_length=256, verbose_name="название статьи", null=False, )
    type_of_publication = models.CharField(max_length=255, verbose_name="тип публикации",
                                           choices=TYPES_OF_PUBLICATIONS, )
    edition = models.CharField(max_length=255, verbose_name="издание", null=False)
    published_year = models.PositiveIntegerField(validators=
                                                 [MaxValueValidator(datetime.now().year),
                                                  MinValueValidator(1921)], verbose_name="год публикации",
                                                 null=False)
    range = models.CharField(max_length=255, verbose_name='диапазон', null=False)
    uk_number = models.IntegerField(verbose_name='номер УК', null=False)

    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        """ По умолчанию записи на главной странице отсортированы по дате публикации, сначала - самые новые"""
        ordering = ('-published_year',)
