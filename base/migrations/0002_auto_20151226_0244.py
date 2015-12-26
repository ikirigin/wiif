# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meal',
            name='created_at',
        ),
        migrations.AddField(
            model_name='meal',
            name='date',
            field=models.DateField(null=True, db_index=True),
        ),
    ]
