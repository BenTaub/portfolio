# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-10-12 22:18
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('balancer', '0005_auto_20171007_1205'),
    ]

    operations = [
        migrations.CreateModel(
            name='account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True)),
                ('institution', models.TextField(blank=True, verbose_name='Financial Institution')),
                ('Account Number', models.TextField(blank=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('Open Date', models.DateField()),
                ('Close Date', models.DateField(blank=True, null=True)),
                ('effective_dt',
                 models.DateTimeField(auto_now=True, help_text='The date & time on which this record became active',
                                      verbose_name='Record effective date')),
            ],
        ),
        migrations.CreateModel(
            name='holding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField(blank=True, null=True)),
                ('num_shares', models.DecimalField(decimal_places=2, max_digits=8)),
                ('As Of', models.DateField()),
                ('effective_dt',
                 models.DateTimeField(auto_now=True, help_text='The date & time on which this record became active',
                                      verbose_name='Record effective date')),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                              to='balancer.account')),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='balancer.Security')),
            ],
        ),
        migrations.AlterField(
            model_name='securityprice',
            name='price_dt',
            field=models.DateField(verbose_name='Price Date'),
        ),
    ]