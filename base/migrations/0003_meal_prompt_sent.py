# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20151226_0244'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='prompt_sent',
            field=models.BooleanField(default=False),
        ),
    ]
