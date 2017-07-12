# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-12 13:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0037_auto_20170711_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='category',
            field=models.CharField(choices=[('of', 'Oferta de materiales'), ('de', 'Demanda de materiales'), ('ac', 'Lote activado'), ('re', 'Lote recuperado')], default='de', help_text='¿Ofreces o necesitas materiales?', max_length=2, verbose_name='¿Oferta o demanda?'),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='category',
            field=models.CharField(choices=[('TR', 'Materiales transferidos'), ('RE', 'Materiales recibidos')], default='TR', max_length=2),
        ),
        migrations.AlterField(
            model_name='space',
            name='nodes',
            field=models.ManyToManyField(help_text="¿Qué nodos de la red participan en este espacio? Mantén presionado 'Control' o 'Command' en un Mac, para seleccionar más de una opción.", related_name='spaces', to='models.Node', verbose_name='Nodos'),
        ),
    ]
