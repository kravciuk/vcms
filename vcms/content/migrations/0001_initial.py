# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import vcms.content.models
import ckeditor.fields
from django.conf import settings
import ckeditor_uploader.fields
import django.utils.timezone
import taggit_autosuggest.managers


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(default='', verbose_name='Name', max_length=100)),
                ('slug', models.SlugField(verbose_name='Slug', max_length=100)),
                ('meta_keywords', models.CharField(blank=True, default='', verbose_name='Meta keywords', max_length=255)),
                ('meta_description', models.CharField(blank=True, default='', verbose_name='Meta description', max_length=255)),
                ('enabled', models.BooleanField(default=True, verbose_name='Enabled')),
                ('hidden', models.BooleanField(default=False, verbose_name='Is hidden')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('path', models.CharField(unique=True, max_length=255)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('title', models.CharField(default='', verbose_name='Title', max_length=255)),
                ('url', models.CharField(db_index=True, default='', editable=False, verbose_name='Path', max_length=255)),
                ('slug', models.SlugField(verbose_name='Slug', max_length=255)),
                ('meta_keywords', models.CharField(blank=True, default='', verbose_name='Meta keywords', max_length=255)),
                ('meta_description', models.CharField(blank=True, default='', verbose_name='Meta description', max_length=255)),
                ('enabled', models.BooleanField(db_index=True, default=True, verbose_name='Enabled')),
                ('hidden', models.BooleanField(db_index=True, default=False, verbose_name='Is hidden')),
                ('type', models.CharField(db_index=True, default='page', choices=[('page', 'Page'), ('gallery', 'Gallery')], max_length=64)),
                ('image', models.ImageField(blank=True, upload_to=vcms.content.models.get_upload_path)),
                ('date_published', models.DateField(db_index=True, default=django.utils.timezone.now, verbose_name='Date published')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, verbose_name='Content')),
                ('rating', models.IntegerField(default=0, verbose_name='Rating')),
                ('show_count', models.IntegerField(default=0, verbose_name='Show count')),
                ('view_count', models.IntegerField(default=0, verbose_name='View count')),
                ('category', models.ForeignKey(null=True, blank=True, to='content.Category', verbose_name='Category')),
            ],
            options={
                'verbose_name': 'Content',
                'verbose_name_plural': 'Content',
            },
        ),
        migrations.CreateModel(
            name='Snippet',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('slug', models.SlugField(verbose_name='Slug', max_length=255)),
                ('title', models.CharField(default='', verbose_name='Title', max_length=255)),
                ('content', ckeditor.fields.RichTextField(blank=True, verbose_name='Content')),
            ],
            options={
                'verbose_name': 'Snippet',
                'verbose_name_plural': 'Snippet',
            },
        ),
        migrations.CreateModel(
            name='PostTag',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('taggit.tag',),
        ),
        migrations.CreateModel(
            name='PostTaggedItem',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('taggit.taggeditem',),
        ),
        migrations.AddField(
            model_name='content',
            name='tags',
            field=taggit_autosuggest.managers.TaggableManager(blank=True, verbose_name='Tags', through='content.PostTaggedItem', to='taggit.Tag', help_text='A comma-separated list of tags.'),
        ),
        migrations.AddField(
            model_name='content',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
