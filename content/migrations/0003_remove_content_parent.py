# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_content_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='content',
            name='parent',
        ),
    ]
