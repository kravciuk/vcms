# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-29 23:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0003_auto_20161230_0101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='share',
            name='time_delete',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]