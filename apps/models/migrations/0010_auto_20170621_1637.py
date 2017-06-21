# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-21 16:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0009_material'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='weight',
            field=models.PositiveIntegerField(blank=True, help_text='Especifica el peso por unidad en kilogramos de manera aproximada. Se usará para hacer cálculos de materiales recuperados y puestos en uso', null=True, verbose_name='Peso unitario'),
        ),
    ]