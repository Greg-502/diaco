# Generated by Django 3.1.7 on 2021-04-15 03:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('denuncias', '0006_auto_20210414_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quejas',
            name='creacion',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 14, 21, 7, 53, 326022)),
        ),
    ]
