# Generated by Django 2.0.3 on 2018-05-29 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('raise_2', '0003_auto_20180523_2014'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buy',
            name='share',
        ),
        migrations.RemoveField(
            model_name='buy',
            name='user',
        ),
    ]
