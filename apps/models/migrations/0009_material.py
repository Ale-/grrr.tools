# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-21 16:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0008_auto_20170619_1904'),
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Nombre')),
                ('creation_date', models.DateField(blank=True, editable=False, null=True)),
                ('slug', models.SlugField(blank=True, editable=False)),
                ('image', models.ImageField(blank=True, upload_to='images/materials/', verbose_name='Imagen')),
                ('family', models.CharField(choices=[('MAD', 'Madera'), ('MET', 'Metal'), ('PLA', 'Plástico'), ('ELE', 'Electrónico'), ('TEX', 'Textiles'), ('OTR', 'Otros')], default='MAD', help_text='Específica la familia del material.', max_length=3, verbose_name='Familia')),
                ('subfamily', models.CharField(choices=[('LO', 'Longitudinales'), ('SU', 'Superficiales'), ('CO', 'Contenedores'), ('OT', 'Otros')], default='LO', help_text='Específica el tipo de material.', max_length=2, verbose_name='Tipo')),
                ('description', models.TextField(blank=True, verbose_name='Descripción')),
                ('unit', models.CharField(blank=True, default='Unidades', help_text="Especifica aquí opcionalmente la unidad a usar cuando se cuantifica este material. Por ejemplo 'metros cuadrados' o 'unidades'", max_length=128, verbose_name='Unidad')),
                ('weight', models.IntegerField(blank=True, help_text='Especifica el peso por unidad en kilogramos de manera aproximada. Se usará para hacer cálculos de materiales recuperados y puestos en uso', null=True, verbose_name='Peso unitario')),
            ],
        ),
    ]
