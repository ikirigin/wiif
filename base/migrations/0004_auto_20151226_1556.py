# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0003_meal_prompt_sent'),
    ]

    operations = [
        migrations.CreateModel(
            name='MealQueried',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(null=True, db_index=True)),
                ('meal_time', models.CharField(max_length=1, choices=[(b'B', b'breakfast'), (b'L', b'lunch'), (b'D', b'dinner')])),
                ('sent_at', models.DateTimeField(db_index=True, auto_now_add=True, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WifeNotified',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sent_at', models.DateTimeField(db_index=True, auto_now_add=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='meal',
            name='prompt_sent',
        ),
        migrations.AddField(
            model_name='meal',
            name='created_at',
            field=models.DateTimeField(db_index=True, auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='wifenotified',
            name='meal',
            field=models.ForeignKey(to='base.Meal'),
        ),
        migrations.AddField(
            model_name='wifenotified',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
