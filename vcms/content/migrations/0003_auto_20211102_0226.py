# Generated by Django 3.2.8 on 2021-11-02 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_auto_20211031_2011'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='share',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='share',
            name='type',
        ),
        migrations.RemoveField(
            model_name='share',
            name='user',
        ),
        migrations.AlterField(
            model_name='content',
            name='json',
            field=models.JSONField(default={}, editable=False, verbose_name='Json content'),
        ),
        migrations.DeleteModel(
            name='File',
        ),
        migrations.DeleteModel(
            name='Pygment',
        ),
        migrations.DeleteModel(
            name='Share',
        ),
    ]
