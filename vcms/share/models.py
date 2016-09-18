# -*- coding: utf-8 -*-
__author__ = 'Vadim'

import os
from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from taggit_autosuggest.managers import TaggableManager
from markdown import markdown
from hashids import Hashids
from datetime import datetime

SHARE_UPLOADED_DIR = settings.VCMS_SHARE_UPLOADED_DIR
SHARE_PROTECTED_DIR = settings.VCMS_SHARE_PROTECTED_DIR


# def upload_path(instance, filename):
#     filename, file_extension = os.path.splitext(filename)
#     if file_extension:
#         filename = "%s%s" % (slugify(filename), file_extension)
#
#     today = datetime.now()
#     upload_path = os.path.join(settings.MEDIA_ROOT, SHARE_UPLOADED_DIR)
#     path = os.path.join(upload_path, "%s/%s/%s" % (today.year, today.month, today.day))
#
#     if not os.path.exists(path):
#         os.makedirs(path)
#
#     return "%s/%s" % (path, filename)


class Share(models.Model):
    PYGMENTS_CHOISE = (
        ('text', 'Plain text'),
        ('python', 'Python'),
        ('php', 'PHP'),
        ('bash', 'Bash'),
        ('html', 'HTML'),
        ('django', 'Django'),
        ('smarty', 'Smarty'),

        ('mysql', 'Mysql'),
        ('postgresql', 'Postgresql'),

        ('csharp', 'C#'),
        ('lua', 'Lua'),
        ('perl', 'Perl'),
        ('ruby', 'Ruby'),
        ('tcl', 'Tcl'),
        ('scheme', 'Scheme'),
        ('xml', 'XML'),
    )

    user = models.ForeignKey(User, default=1)
    type = models.CharField(max_length=10, verbose_name=_(u'Type'), choices=PYGMENTS_CHOISE, default='text', db_index=True)
    title = models.CharField(_(u'Title'),max_length=255, blank=True, null=True)
    slug = models.SlugField(_(u'Slug'),max_length=255, blank=True, null=True, db_index=True)
    file = models.FileField(max_length=255, blank=True, null=True, upload_to=SHARE_UPLOADED_DIR)
    url = models.CharField(_(u'Url'),max_length=255, blank=True, null=True)
    tags = TaggableManager(_(u'Tags'), blank=True)
    description = models.TextField(_(u'Description'), blank=True, null=True)
    content = models.TextField(_(u'Content'), blank=True, null=True)
    password = models.CharField(max_length=64, blank=True, db_index=True)
    disabled = models.BooleanField(default=False, db_index=True)
    hidden = models.BooleanField(default=False, db_index=True)

    views = models.IntegerField(default=0, editable=False)
    file_name = models.CharField(max_length=128, blank=True, null=True)
    thumbnail = models.CharField(max_length=255, null=True, editable=False)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now_add=True)
    content_html = models.TextField(editable=False, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.description is not None:
            self.description_html = markdown(self.description, ['codehilite'])

        if not self.pk:
            expl = self.title.split('/')
            if len(expl) > 1:
                self.title = expl[0]
                self.slug = self.unique_slug(slugify(expl[1]))

        if not self.title and self.file_name:
            if self.file_type == 'image':
                file_type = 'Picture'
            else:
                file_type = 'File'
            self.title = _(u'%s: %s' % (file_type, self.file_name))
        elif not self.title and self.url:
            self.title = _(u'Url to: %s %s' % (self.url[:32], '...' if len(self.url) > 32 else ''))

        self.type = self.file_type()
        self.get_title()

        super(Share, self).save()

        if self.slug is None:
            self.slug = self.short_id
            super(Share, self).save()

    def process_file(self):
        filename, file_extension = os.path.splitext(self.file)
        file_name = "%s%s" % (slugify(filename), file_extension)

    @property
    def download_url(self):
        return reverse('share_download_file', args=[self.short_id])

    @property
    def base_url(self):
        return reverse('share_snippet', args=[self.short_id])

    @property
    def redirect_url(self):
        return reverse('share_link_redirect', args=[self.short_id])

    @property
    def view(self):
        if self.url and self.video_link is False:
            return self.redirect_url
        else:
            return self.base_url

    def get_title(self):
        if self.title is None or self.title.strip() == '':
            self.title = "%s - %s" % (_(u'Snippet'), self.type)

    def unique_slug(self, slug, counter=0):
        if counter > 0:
            unique_slug = "%s%s" % (slug, counter)
        else:
            unique_slug = slug

        if self.id:
            my_id = self.id
        else:
            my_id = 0
        rs = self._default_manager.filter(slug=unique_slug).exclude(id=my_id)
        if rs:
            counter += 1
            return self.unique_slug(slug, counter)
        else:
            return unique_slug

    @property
    def short_id(self):
        if self.slug:
            return self.slug
        else:
            hashids = Hashids(salt=settings.SECRET_KEY, min_length=4)
            return hashids.encrypt(self.id)

    def get_absolute_url(self):
        return '/%s/%s' % ('share', self.short_id)

    def file_type(self):
        if self.file_name is not None:
            filename, file_extension = os.path.splitext(self.file_name)
            if file_extension.lower() in ['.jpg', '.jpeg', '.gif', '.png']:
                return 'image'
            else:
                return 'file'
        return self.type

    @property
    def video_link(self):
        if self.url is not None:
            if self.url.find('youtube'):
                return True
        return False

    def __str__(self):
        return self.title

