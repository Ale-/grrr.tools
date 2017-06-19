# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-12 10:57
from __future__ import unicode_literals

from django.db import migrations, models
import djgeojson.fields


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0002_auto_20170609_1840'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='address',
            field=models.CharField(blank=True, help_text='Dirección del nodo. No es necesario que incluyas la localidad anterior.', max_length=128, null=True, verbose_name='Dirección'),
        ),
        migrations.AlterField(
            model_name='node',
            name='geom',
            field=djgeojson.fields.PointField(help_text='Añade la ubicación del nodo. Usa el botón inferior para localizar el punto a partir de la localidad y dirección introducidos anteriormente. Podrás ajustar posteriormente el punto arrastrándolo.', null=True, verbose_name='Ubicación'),
        ),
    ]