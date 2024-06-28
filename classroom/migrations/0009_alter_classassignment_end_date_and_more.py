# Generated by Django 5.0.6 on 2024-06-10 14:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0008_alter_classassignment_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classassignment',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2025, 6, 10, 14, 52, 56, 56420, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='studentmarks',
            name='semester',
            field=models.IntegerField(default=1),
        ),
    ]
