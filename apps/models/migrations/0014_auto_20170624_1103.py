# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-24 11:03
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0013_sms'),
    ]

    operations = [
        migrations.AddField(
            model_name='reuse',
            name='active',
            field=models.BooleanField(default=True, help_text='¿Este reuso es un proceso en marcha o se da por finalizado?', verbose_name='Activo'),
        ),
        migrations.AlterField(
            model_name='sms',
            name='date',
            field=models.DateField(blank=True, default=datetime.date.today, editable=False),
        ),
    ]
