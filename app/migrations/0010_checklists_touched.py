# Generated by Django 2.0.7 on 2018-07-28 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_checklists_is_visible'),
    ]

    operations = [
        migrations.AddField(
            model_name='checklists',
            name='touched',
            field=models.BooleanField(default=False),
        ),
    ]