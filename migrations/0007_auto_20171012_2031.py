# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-10-13 01:31
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('balancer', '0006_auto_20171012_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holding',
            name='account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='balancer.Account'),
        ),
    ]