# Generated by Django 2.0.13 on 2019-06-07 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0036_auto_20190607_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deal',
            name='term',
            field=models.TextField(),
        ),
    ]
