# Generated by Django 3.2.8 on 2021-10-31 20:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit_autosuggest.managers
import vu.abstract.models


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', vu.abstract.models.UniqueFileField(upload_to='share/%Y/%m/%d', verbose_name='File')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('mime', models.CharField(blank=True, max_length=128, null=True)),
                ('width', models.IntegerField(default=0)),
                ('height', models.IntegerField(default=0)),
                ('thumbnail', models.CharField(blank=True, max_length=255, null=True)),
                ('size', models.IntegerField(default=0)),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Comments')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
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
        migrations.CreateModel(
            name='Share',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Title')),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, verbose_name='Slug')),
                ('url', models.CharField(blank=True, max_length=255, null=True, verbose_name='Url')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('content', models.TextField(blank=True, null=True, verbose_name='Content')),
                ('password', models.CharField(blank=True, db_index=True, max_length=64)),
                ('disabled', models.BooleanField(db_index=True, default=False)),
                ('hidden', models.BooleanField(db_index=True, default=False)),
                ('personal', models.BooleanField(default=False, verbose_name='Personal')),
                ('json', models.JSONField(default={}, verbose_name='Json content')),
                ('expired_on', models.DateField(default='2099-01-01', verbose_name='Expired on')),
                ('view_count', models.IntegerField(default=0, editable=False)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('time_updated', models.DateTimeField(auto_now=True)),
                ('time_delete', models.DateField(blank=True, default=None, null=True)),
                ('tags', taggit_autosuggest.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', related_name='share_tags', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='content.pygment', verbose_name='Pygment type')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='share_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Snippet',
        ),
        migrations.AlterField(
            model_name='content',
            name='tags',
            field=taggit_autosuggest.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', related_name='content_tags', through='content.PostTaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='content',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='file',
            name='share',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='file_share', to='content.share'),
        ),
        migrations.AddField(
            model_name='file',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='file_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
