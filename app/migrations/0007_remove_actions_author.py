# Generated by Django 2.0.5 on 2018-07-17 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20180717_1541'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actions',
            name='author',
        ),
    ]
