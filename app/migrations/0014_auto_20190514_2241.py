# Generated by Django 2.0.13 on 2019-05-14 19:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20190514_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='date',
            field=models.DateField(default=datetime.datetime(2019, 5, 14, 19, 41, 27, 683972, tzinfo=utc)),
        ),
    ]
