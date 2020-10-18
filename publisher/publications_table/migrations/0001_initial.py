# Generated by Django 3.1.2 on 2020-10-18 11:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='имя')),
                ('surname', models.CharField(max_length=255, unique=True, verbose_name='фамилия')),
                ('patronymic', models.CharField(max_length=255, verbose_name='отчество')),
                ('work_position', models.CharField(max_length=255, verbose_name='должность')),
                ('military_rank', models.CharField(max_length=255, verbose_name='звание')),
            ],
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='название статьи')),
                ('type_of_publication', models.CharField(choices=[('Тезис', 'Тезис'), ('Статья', 'Статья')], max_length=255, verbose_name='тип публикации')),
                ('edition', models.CharField(max_length=255, verbose_name='издание')),
                ('published_year', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(2020), django.core.validators.MinValueValidator(1921)], verbose_name='год публикации')),
                ('range', models.CharField(max_length=255, verbose_name='диапазон')),
                ('uk_number', models.IntegerField(verbose_name='номер УК')),
                ('authors', models.ManyToManyField(to='publications_table.Author', verbose_name='авторы')),
            ],
            options={
                'ordering': ('-published_year',),
            },
        ),
    ]