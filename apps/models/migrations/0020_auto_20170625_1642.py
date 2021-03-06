# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-25 16:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0019_batch'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='grrr_blog',
            field=models.BooleanField(default=False, verbose_name='Blog de la página'),
        ),
        migrations.AddField(
            model_name='post',
            name='space',
            field=models.ForeignKey(help_text='¿Al blog de qué espacio está asociado este post?', null=True, on_delete=django.db.models.deletion.CASCADE, to='models.Space', verbose_name='Espacio'),
        ),
        migrations.AlterField(
            model_name='batch',
            name='expiration',
            field=models.DateField(blank=True, help_text='Fecha límite para acceder a la oferta asociada. Usa el formato dd/mm/aaaa, por ejemplo: 01/05/2015.', null=True, verbose_name='Fecha de expiración'),
        ),
        migrations.AlterField(
            model_name='batch',
            name='material',
            field=models.ForeignKey(help_text='El material del que se compone el lote', null=True, on_delete=django.db.models.deletion.SET_NULL, to='models.Material', verbose_name='Material'),
        ),
    ]
