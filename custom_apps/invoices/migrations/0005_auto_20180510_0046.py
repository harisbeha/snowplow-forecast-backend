# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-10 04:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0004_auto_20180509_1440'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvoiceProxyPrelim',
            fields=[
            ],
            options={
                'verbose_name': 'Preliminary Invoices',
                'abstract': False,
                'proxy': True,
                'indexes': [],
            },
            bases=('invoices.invoice',),
        ),
        migrations.AddField(
            model_name='building',
            name='vendor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='vendor_locations', to='invoices.Building'),
            preserve_default=False,
        ),
    ]
