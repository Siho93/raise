# Generated by Django 2.0.3 on 2018-06-10 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raise_2', '0016_auto_20180610_1804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='monat',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='history',
            name='wert',
            field=models.FloatField(default=0),
        ),
    ]
