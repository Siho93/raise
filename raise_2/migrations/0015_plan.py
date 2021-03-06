# Generated by Django 2.0.3 on 2018-06-06 17:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('raise_2', '0014_auto_20180605_2321'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField(default=0)),
                ('volume', models.FloatField()),
                ('value', models.FloatField()),
                ('share', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='raise_2.Shares')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
