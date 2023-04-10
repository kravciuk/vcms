# Generated by Django 4.1.7 on 2023-03-14 22:26

from django.db import migrations, models
import vcms.share.models


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0005_file_processed_file_updated_at_alter_share_json'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='height',
        ),
        migrations.RemoveField(
            model_name='file',
            name='size',
        ),
        migrations.RemoveField(
            model_name='file',
            name='thumbnail',
        ),
        migrations.RemoveField(
            model_name='file',
            name='width',
        ),
        migrations.AddField(
            model_name='file',
            name='json',
            field=models.JSONField(default=vcms.share.models.default_json, verbose_name='Json content'),
        ),
    ]