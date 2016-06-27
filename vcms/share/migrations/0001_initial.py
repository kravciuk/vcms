# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import taggit_autosuggest.managers


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Share',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('type', models.CharField(db_index=True, default='text', choices=[('text', 'Plain text'), ('python', 'Python'), ('php', 'PHP'), ('bash', 'Bash'), ('html', 'HTML'), ('django', 'Django'), ('smarty', 'Smarty'), ('mysql', 'Mysql'), ('postgresql', 'Postgresql'), ('csharp', 'C#'), ('lua', 'Lua'), ('perl', 'Perl'), ('ruby', 'Ruby'), ('tcl', 'Tcl'), ('scheme', 'Scheme'), ('xml', 'XML')], verbose_name='Type', max_length=10)),
                ('title', models.CharField(null=True, blank=True, verbose_name='Title', max_length=255)),
                ('slug', models.SlugField(null=True, blank=True, verbose_name='Slug', max_length=255)),
                ('file', models.FileField(null=True, blank=True, upload_to='share', max_length=255)),
                ('url', models.CharField(null=True, blank=True, verbose_name='Url', max_length=255)),
                ('description', models.TextField(null=True, blank=True, verbose_name='Description')),
                ('content', models.TextField(null=True, blank=True, verbose_name='Content')),
                ('password', models.CharField(blank=True, db_index=True, max_length=64)),
                ('disabled', models.BooleanField(db_index=True, default=False)),
                ('hidden', models.BooleanField(db_index=True, default=False)),
                ('views', models.IntegerField(default=0, editable=False)),
                ('file_name', models.CharField(null=True, blank=True, max_length=128)),
                ('thumbnail', models.CharField(null=True, editable=False, max_length=255)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('time_updated', models.DateTimeField(auto_now_add=True)),
                ('content_html', models.TextField(null=True, blank=True, editable=False)),
                ('tags', taggit_autosuggest.managers.TaggableManager(blank=True, verbose_name='Tags', through='taggit.TaggedItem', to='taggit.Tag', help_text='A comma-separated list of tags.')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, default=1)),
            ],
        ),
    ]
