# Generated by Django 2.0.3 on 2018-06-01 13:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('raise_2', '0008_auto_20180530_1008'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
