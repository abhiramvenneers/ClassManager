# Generated by Django 5.0.6 on 2024-06-10 16:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0024_alter_classassignment_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classassignment',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2025, 6, 10, 16, 39, 31, 401174, tzinfo=datetime.timezone.utc)),
        ),
    ]
