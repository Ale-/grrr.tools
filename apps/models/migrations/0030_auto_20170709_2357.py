# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-09 23:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0029_auto_20170709_2310'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sms',
            name='replies',
        ),
        migrations.AddField(
            model_name='sms',
            name='replies',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='models.Sms'),
        ),
    ]
