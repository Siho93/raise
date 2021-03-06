# Generated by Django 2.0.3 on 2018-05-23 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raise_2', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shares',
            old_name='value',
            new_name='dividende',
        ),
        migrations.AddField(
            model_name='shares',
            name='art',
            field=models.CharField(default='aktie', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shares',
            name='jahrlowhigh',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shares',
            name='kürzel',
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shares',
            name='lowhigh',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shares',
            name='openclose',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shares',
            name='volumen',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shares',
            name='wert',
            field=models.FloatField(default=0),
        ),
    ]
