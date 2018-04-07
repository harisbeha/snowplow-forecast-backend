# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-07 22:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('identifier', models.TextField(max_length=50, verbose_name='identifier for the building, e.g. TDE1234')),
                ('address', models.TextField(max_length=200, verbose_name='street address')),
                ('city', models.TextField(max_length=50, verbose_name='city name')),
                ('state', models.TextField(max_length=2, verbose_name='state abbreviation')),
                ('zip', models.TextField(max_length=15, verbose_name='zip code')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('invoice_number', models.IntegerField(verbose_name='numerical identifier for the invoice')),
                ('remission_address', models.TextField(verbose_name='full mailing addresses to send remission')),
                ('first_event', models.DateTimeField(verbose_name='date of the first storm event in this invoice')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('response_time_start', models.DateTimeField(verbose_name='time clocked in')),
                ('response_time_end', models.DateTimeField(verbose_name='time clocked out')),
                ('provided_deicing', models.BooleanField(verbose_name='whether de-icing services were provided')),
                ('provided_plowing', models.BooleanField(verbose_name='whether plowing services were provided')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.TextField(verbose_name='company name of the vendor')),
                ('address', models.TextField(max_length=200, verbose_name='full mailing address')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WorkOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('order_number', models.TextField(max_length=50, verbose_name='textual work order number, e.g. TDU12345678')),
                ('deice_rate', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='cost in dollars without tax per de-icing service')),
                ('deice_tax', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='tax in dollars per de-icing service')),
                ('plow_rate', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='cost in dollars without tax per plow service, includes plowing and shoveling only')),
                ('plow_tax', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='tax in dollars per plow service, includes plowing and shoveling only')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoices.Invoice')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='job',
            name='work_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoices.WorkOrder'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoices.Vendor'),
        ),
        migrations.AlterUniqueTogether(
            name='workorder',
            unique_together=set([('invoice', 'order_number')]),
        ),
        migrations.AlterUniqueTogether(
            name='invoice',
            unique_together=set([('vendor', 'invoice_number')]),
        ),
    ]
