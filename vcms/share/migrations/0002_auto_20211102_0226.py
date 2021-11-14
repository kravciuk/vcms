# Generated by Django 3.2.8 on 2021-11-02 02:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pygment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='Name')),
                ('code', models.CharField(max_length=16, verbose_name='Code')),
                ('enabled', models.BooleanField(default=True, verbose_name='Enabled')),
            ],
            options={
                'verbose_name': 'Pygment type',
                'verbose_name_plural': 'Pygment types',
            },
        ),
        migrations.AlterField(
            model_name='share',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='share.pygment', verbose_name='Pygment type'),
        ),
    ]
