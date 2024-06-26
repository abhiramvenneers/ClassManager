# Generated by Django 5.0.6 on 2024-06-10 16:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0015_alter_classassignment_end_date_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='studentmarks',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='classassignment',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2025, 6, 10, 16, 12, 59, 635435, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='studentmarks',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
