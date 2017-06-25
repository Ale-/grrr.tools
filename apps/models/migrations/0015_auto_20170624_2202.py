# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-24 22:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0014_auto_20170624_1103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reuse',
            name='active',
            field=models.BooleanField(default=True, help_text='¿Este reuso es un proceso en marcha o se da por finalizado? Los proyectos en marcha tienen mayor visibilidad en la plataforma.', verbose_name='Activo'),
        ),
    ]
