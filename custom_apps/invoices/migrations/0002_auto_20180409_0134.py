# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-09 01:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vendorsettings',
            options={'verbose_name_plural': 'vendor settings'},
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_number',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='numerical identifier for the invoice'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='remission_address',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='full mailing addresses to send remission'),
        ),
        migrations.AlterField(
            model_name='job',
            name='haul_stack_estimate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='cost estimate for future snow hauling or stacking'),
        ),
        migrations.AlterField(
            model_name='job',
            name='safety_concerns',
            field=models.TextField(blank=True, max_length=1000, verbose_name='any concerns? let us know of all site conditions'),
        ),
        migrations.AlterField(
            model_name='job',
            name='snow_instructions',
            field=models.TextField(blank=True, max_length=1000, verbose_name='extra instructions for handling remaining snow'),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='invoice',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='invoices.Invoice'),
        ),
    ]
