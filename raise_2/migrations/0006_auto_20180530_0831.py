# Generated by Django 2.0.3 on 2018-05-30 06:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('raise_2', '0005_buy_aktie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buy',
            name='aktie',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='raise_2.Shares'),
        ),
    ]
