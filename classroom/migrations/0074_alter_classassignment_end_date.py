# Generated by Django 5.0.6 on 2024-06-16 11:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0073_alter_classassignment_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classassignment',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2025, 6, 16, 11, 18, 40, 808137, tzinfo=datetime.timezone.utc)),
        ),
    ]
