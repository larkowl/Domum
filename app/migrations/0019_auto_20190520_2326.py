# Generated by Django 2.0.13 on 2019-05-20 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20190516_2342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
