# Generated by Django 3.1.2 on 2020-10-23 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publications_table', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ('surname',)},
        ),
    ]