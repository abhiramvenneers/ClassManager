# Generated by Django 5.0.6 on 2024-06-11 13:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0042_alter_classassignment_end_date_vivamarks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classassignment',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2025, 6, 11, 13, 45, 29, 299725, tzinfo=datetime.timezone.utc)),
        ),
        migrations.DeleteModel(
            name='VivaMarks',
        ),
    ]
