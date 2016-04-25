# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='share',
            name='file',
            field=models.FileField(max_length=255, null=True, upload_to=b'share', blank=True),
        ),
    ]
