# Generated by Django 3.1.7 on 2021-06-30 23:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('denuncias', '0002_auto_20210423_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quejas',
            name='creacion',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 30, 17, 41, 20, 844355)),
        ),
    ]