# Generated by Django 2.0.13 on 2019-05-11 10:43

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20190511_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='date',
            field=models.DateField(default=datetime.datetime(2019, 5, 11, 10, 43, 42, 45015, tzinfo=utc)),
        ),
    ]