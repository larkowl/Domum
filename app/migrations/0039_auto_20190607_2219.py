# Generated by Django 2.0.13 on 2019-06-07 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0038_auto_20190607_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='1',
            field=models.ImageField(blank=True, null=True, upload_to='images/announcements/'),
        ),
        migrations.AlterField(
            model_name='announcement',
            name='2',
            field=models.ImageField(blank=True, null=True, upload_to='images/announcements/'),
        ),
        migrations.AlterField(
            model_name='announcement',
            name='3',
            field=models.ImageField(blank=True, null=True, upload_to='images/announcements/'),
        ),
        migrations.AlterField(
            model_name='announcement',
            name='4',
            field=models.ImageField(blank=True, null=True, upload_to='images/announcements/'),
        ),
        migrations.AlterField(
            model_name='announcement',
            name='5',
            field=models.ImageField(blank=True, null=True, upload_to='images/announcements/'),
        ),
        migrations.AlterField(
            model_name='announcement',
            name='6',
            field=models.ImageField(blank=True, null=True, upload_to='images/announcements/'),
        ),
    ]
