# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-09 23:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0028_auto_20170709_2049'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sms',
            name='reply',
        ),
        migrations.AddField(
            model_name='sms',
            name='replies',
            field=models.ManyToManyField(blank=True, related_name='_sms_replies_+', to='models.Sms'),
        ),
    ]
