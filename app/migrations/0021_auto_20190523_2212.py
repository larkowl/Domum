# Generated by Django 2.0.13 on 2019-05-23 19:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_auto_20190523_0023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='person',
            name='last_name',
        ),
    ]