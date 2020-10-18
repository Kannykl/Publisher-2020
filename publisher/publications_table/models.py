from django.db import models


class Author(models.Model):
    """Автор статьи"""
    name = models.CharField(max_length=255, null=False, verbose_name="имя")
    surname = models.CharField(max_length=255, null=False, unique=True, verbose_name="фамилия")
    patronymic = models.CharField(max_length=255, null=False, verbose_name="отчество")
    work_position = models.CharField(max_length=255, null=False, verbose_name="должность")
    military_rank = models.CharField(max_length=255, null=False, verbose_name="звание")

    def __str__(self):
        return self.surname
