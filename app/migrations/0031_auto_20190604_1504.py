# Generated by Django 2.0.13 on 2019-06-04 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0030_person_ava'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='ava',
            field=models.ImageField(blank=True, null=True, upload_to='images/avas/'),
        ),
    ]
