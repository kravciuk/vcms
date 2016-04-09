# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import vcms.content.models
import ckeditor.fields
import django.utils.timezone
from django.conf import settings
import django.contrib.postgres.fields.hstore
import taggit_autosuggest.managers
import ckeditor_uploader.fields


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=100, verbose_name='Name')),
                ('slug', models.SlugField(max_length=100, verbose_name='Slug')),
                ('meta_keywords', models.CharField(default=b'', max_length=255, verbose_name='Meta keywords', blank=True)),
                ('meta_description', models.CharField(default=b'', max_length=255, verbose_name='Meta description', blank=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.CharField(unique=True, max_length=255)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('title', models.CharField(default=b'', max_length=255, verbose_name='Title')),
                ('url', models.CharField(default=b'', verbose_name='Path', max_length=255, editable=False, db_index=True)),
                ('slug', models.SlugField(max_length=255, verbose_name='Slug')),
                ('meta_keywords', models.CharField(default=b'', max_length=255, verbose_name='Meta keywords', blank=True)),
                ('meta_description', models.CharField(default=b'', max_length=255, verbose_name='Meta description', blank=True)),
                ('enabled', models.BooleanField(default=True, db_index=True, verbose_name='Enabled')),
                ('hidden', models.BooleanField(default=False, db_index=True, verbose_name='Is hidden')),
                ('custom', django.contrib.postgres.fields.hstore.HStoreField(null=True, blank=True)),
                ('type', models.CharField(default=b'page', max_length=64, db_index=True, choices=[(b'page', 'Page'), (b'news', 'News'), (b'gallery', 'Gallery')])),
                ('image', models.ImageField(upload_to=vcms.content.models.get_upload_path, blank=True)),
                ('date_published', models.DateField(default=django.utils.timezone.now, verbose_name='Date published', db_index=True)),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Content', blank=True)),
                ('rating', models.IntegerField(default=0, verbose_name='Rating')),
                ('show_count', models.IntegerField(default=0, verbose_name='Show count')),
                ('view_count', models.IntegerField(default=0, verbose_name='View count')),
                ('category', models.ForeignKey(verbose_name='Category', blank=True, to='content.Category', null=True)),
            ],
            options={
                'verbose_name': 'Content',
                'verbose_name_plural': 'Content',
            },
        ),
        migrations.CreateModel(
            name='Snippet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(max_length=255, verbose_name='Slug')),
                ('title', models.CharField(default=b'', max_length=255, verbose_name='Title')),
                ('content', ckeditor.fields.RichTextField(verbose_name='Content', blank=True)),
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
            field=taggit_autosuggest.managers.TaggableManager(to='taggit.Tag', through='content.PostTaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='content',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
