# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-10 12:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0031_auto_20170710_1202'),
    ]

    operations = [
        migrations.AddField(
            model_name='batch',
            name='periodicity',
            field=models.CharField(choices=[('no', 'Ninguna'), ('se', 'Semanal'), ('me', 'Mensual'), ('an', 'Anual')], default='no', help_text='¿Es uan oferta única o tiene periodicidad?', max_length=2, verbose_name='Periodicidad'),
        ),
        migrations.AlterField(
            model_name='batch',
            name='category',
            field=models.CharField(choices=[('of', 'Oferta de materiales'), ('de', 'Demanda de materiales')], default='de', help_text='¿Ofreces o necesitas materiales?', max_length=2, verbose_name='¿Oferta o demanda?'),
        ),
    ]
