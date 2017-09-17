# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-09-16 16:56
from __future__ import unicode_literals

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('balancer', '0002_auto_20170827_1645'),
    ]

    operations = [
        migrations.CreateModel(
            name='SecurityAvailDynamic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('symbol', models.TextField()),
                ('at_dt', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Price Date & Time')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('current_rec_fg',
                 models.BooleanField(default=True, help_text='Set to True for the current version of the record',
                                     verbose_name='Current record flag')),
                ('effective_dt', models.DateTimeField(default=django.utils.timezone.now,
                                                      help_text='The date & time on which this record became active',
                                                      verbose_name='Record effective date')),
                ('end_dt',
                 models.DateTimeField(blank=True, help_text='The date and time on which this record expired', null=True,
                                      verbose_name='Record end date')),
                ('security_avail_static', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE,
                                                            to='balancer.SecurityAvailStatic')),
            ],
        ),
        migrations.RemoveField(
            model_name='securityavail',
            name='security_avail_static',
        ),
        migrations.DeleteModel(
            name='SecurityAvail',
        ),
    ]