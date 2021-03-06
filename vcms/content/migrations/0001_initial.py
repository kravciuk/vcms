# Generated by Django 2.1.4 on 2018-12-23 16:28

import ckeditor.fields
import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import taggit_autosuggest.managers
import vcms.content.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100, verbose_name='Name')),
                ('slug', models.SlugField(max_length=100, verbose_name='Slug')),
                ('meta_keywords', models.CharField(blank=True, default='', max_length=255, verbose_name='Meta keywords')),
                ('meta_description', models.CharField(blank=True, default='', max_length=255, verbose_name='Meta description')),
                ('enabled', models.BooleanField(default=True, verbose_name='Enabled')),
                ('hidden', models.BooleanField(default=False, verbose_name='Is hidden')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255, unique=True)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('title', models.CharField(default='', max_length=255, verbose_name='Title')),
                ('url', models.CharField(db_index=True, default='', editable=False, max_length=255, verbose_name='Path')),
                ('slug', models.SlugField(max_length=255, verbose_name='Slug')),
                ('template', models.CharField(choices=[('content_view', 'View single page'), ('content_list', 'List pages')], default='content_view', max_length=100, verbose_name='Template')),
                ('meta_keywords', models.CharField(blank=True, default='', max_length=255, verbose_name='Meta keywords')),
                ('meta_description', models.CharField(blank=True, default='', max_length=255, verbose_name='Meta description')),
                ('enabled', models.BooleanField(db_index=True, default=True, verbose_name='Enabled')),
                ('hidden', models.BooleanField(db_index=True, default=False, verbose_name='Is hidden')),
                ('type', models.CharField(choices=[('page', 'Page'), ('gallery', 'Gallery')], db_index=True, default='page', max_length=64)),
                ('image', models.ImageField(blank=True, upload_to=vcms.content.models.get_upload_path)),
                ('date_published', models.DateField(db_index=True, default=django.utils.timezone.now, verbose_name='Date published')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, verbose_name='Content')),
                ('comments', models.BooleanField(default=False, verbose_name='Allow comments')),
                ('rating', models.IntegerField(default=0, verbose_name='Rating')),
                ('show_count', models.IntegerField(default=0, verbose_name='Show count')),
                ('view_count', models.IntegerField(default=0, verbose_name='View count')),
                ('category', models.ManyToManyField(blank=True, to='content.Category', verbose_name='Category')),
            ],
            options={
                'verbose_name': 'Content',
                'verbose_name_plural': 'Content',
            },
        ),
        migrations.CreateModel(
            name='Snippet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=255, verbose_name='Slug')),
                ('title', models.CharField(default='', max_length=255, verbose_name='Title')),
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
                'indexes': [],
            },
            bases=('taggit.tag',),
        ),
        migrations.CreateModel(
            name='PostTaggedItem',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('taggit.taggeditem',),
        ),
        migrations.AddField(
            model_name='content',
            name='tags',
            field=taggit_autosuggest.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='content.PostTaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='content',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
