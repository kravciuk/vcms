# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import taggit_autosuggest.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Share',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'text', max_length=10, verbose_name='Type', db_index=True, choices=[(b'text', b'Plain text'), (b'python', b'Python'), (b'php', b'PHP'), (b'bash', b'Bash'), (b'html', b'HTML'), (b'django', b'Django'), (b'smarty', b'Smarty'), (b'mysql', b'Mysql'), (b'postgresql', b'Postgresql'), (b'csharp', b'C#'), (b'lua', b'Lua'), (b'perl', b'Perl'), (b'ruby', b'Ruby'), (b'tcl', b'Tcl'), (b'scheme', b'Scheme'), (b'xml', b'XML')])),
                ('title', models.CharField(max_length=255, null=True, verbose_name='Title', blank=True)),
                ('slug', models.SlugField(max_length=255, null=True, verbose_name='Slug', blank=True)),
                ('file', models.FileField(max_length=255, null=True, upload_to=b'', blank=True)),
                ('url', models.CharField(max_length=255, null=True, verbose_name='Url', blank=True)),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('content', models.TextField(null=True, verbose_name='Content', blank=True)),
                ('password', models.CharField(db_index=True, max_length=64, blank=True)),
                ('disabled', models.BooleanField(default=False, db_index=True)),
                ('hidden', models.BooleanField(default=False, db_index=True)),
                ('views', models.IntegerField(default=0, editable=False)),
                ('file_name', models.CharField(max_length=128, null=True, blank=True)),
                ('thumbnail', models.CharField(max_length=255, null=True, editable=False)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('time_updated', models.DateTimeField(auto_now_add=True)),
                ('content_html', models.TextField(null=True, editable=False, blank=True)),
                ('tags', taggit_autosuggest.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags')),
                ('user', models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
