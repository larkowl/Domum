# Generated by Django 2.0.13 on 2019-06-10 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0042_announcement_metro_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='photo7',
            field=models.ImageField(blank=True, null=True, upload_to='images/announcements/'),
        ),
        migrations.AddField(
            model_name='announcement',
            name='photo8',
            field=models.ImageField(blank=True, null=True, upload_to='images/announcements/'),
        ),
    ]
