# Generated by Django 2.0 on 2017-12-30 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventmap', '0003_remove_event_desc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='mapid',
        ),
        migrations.DeleteModel(
            name='Event',
        ),
    ]
