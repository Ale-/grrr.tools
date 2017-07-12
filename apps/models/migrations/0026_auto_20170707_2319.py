# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-07 23:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0025_batch_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='category',
            field=models.CharField(choices=[('no', 'Ninguna'), ('se', 'Semanal'), ('me', 'Mensual'), ('an', 'Anual')], default='no', help_text='¿Es uan oferta única o tiene periodicidad?', max_length=2, verbose_name='Periodicidad'),
        ),
        migrations.AlterField(
            model_name='batch',
            name='milestones',
            field=models.ManyToManyField(blank=True, to='models.Milestone', verbose_name='Movimientos'),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='category',
            field=models.CharField(choices=[('AC', 'Materiales activados'), ('TR', 'Materiales transferidos'), ('RE', 'Materiales recibidos')], default='TR', max_length=2),
        ),
    ]