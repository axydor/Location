# Generated by Django 2.0 on 2018-01-01 14:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventmap', '0014_auto_20180101_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='timetoann',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
