# Generated by Django 5.1.3 on 2024-11-13 17:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0003_todo_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime.utcnow),
        ),
    ]
