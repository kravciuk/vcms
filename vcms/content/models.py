# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

from datetime import datetime

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.models import Tag, TaggedItem
from taggit_autosuggest.managers import TaggableManager
from treebeard.mp_tree import MP_Node
from vcms.utils import id_to_hash

from vcms.utils import unique_slug

if hasattr(settings, 'VCMS_POST_CUTTER'):
    cutter = settings.VCMS_POST_CUTTER
else:
    cutter = '<!-- cut -->'


class PostTag(Tag):
    class Meta:
        proxy = True

    def slugify(self, tag, i=None):
            slug = slugify(tag.lower())
            if i is not None:
                slug += '-%d' % i
            return slug


class PostTaggedItem(TaggedItem):
    class Meta:
        proxy = True

    @classmethod
    def tag_model(cls):
        return PostTag


def get_upload_path(instance, filename):
    return instance.get_upload_path(filename)


class Category(models.Model):
    name = models.CharField(_(u'Name'), max_length=100, default='')
    slug = models.SlugField(verbose_name=_(u'Slug'), max_length=100)
    meta_keywords = models.CharField(_(u'Meta keywords'), max_length=255, default='', blank=True)
    meta_description = models.CharField(_(u'Meta description'), max_length=255, default='', blank=True)
    enabled = models.BooleanField(_(u'Enabled'), default=True)
    hidden = models.BooleanField(_(u'Is hidden'), default=False)

    class Meta:
        verbose_name = _(u'Category')
        verbose_name_plural = _(u'Categories')
        ordering = ['name']

    def __str__(self):
        return self.name


class Content(MP_Node):
    HASH_LENGTH = 8
    TYPE_PAGE = 'page'
    TYPE_GALLERY = 'gallery'
    type_choices = (
        (TYPE_PAGE, _(u'Page')),
        (TYPE_GALLERY, _(u'Gallery')),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(_(u'Title'), max_length=255, default='')
    url = models.CharField(_(u'Path'), max_length=255, default='', editable=False, db_index=True)
    slug = models.SlugField(verbose_name=_(u'Slug'), max_length=255, db_index=True)
    template = models.CharField(_(u'Template'), choices=settings.VCMS_TEMPLATES, max_length=100, default='content_view')
    meta_keywords = models.CharField(_(u'Meta keywords'), max_length=255, default='', blank=True)
    meta_description = models.CharField(_(u'Meta description'), max_length=255, default='', blank=True)
    enabled = models.BooleanField(_(u'Enabled'), default=True, db_index=True)
    hidden = models.BooleanField(_(u'Is hidden'), default=False, db_index=True)
    category = models.ManyToManyField(Category, verbose_name=_(u'Category'), blank=True)
    type = models.CharField(max_length=64, choices=type_choices, db_index=True, default=TYPE_PAGE)
    image = models.ImageField(upload_to=get_upload_path, blank=True)
    date_published = models.DateField(_(u'Date published'), default=timezone.now, db_index=True)
    content = RichTextUploadingField(_(u'Content'), blank=True)
    comments = models.BooleanField(_(u'Allow comments'), default=False)
    language = models.CharField(_(u'Language'), choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE, max_length=5)

    tags = TaggableManager(_(u'Tags'), through=PostTaggedItem, blank=True)
    rating = models.IntegerField(_(u'Rating'), default=0)
    show_count = models.IntegerField(_(u'Show count'), default=0)
    view_count = models.IntegerField(_(u'View count'), default=0)

    node_order_by = ['date_published']

    class Meta:
        verbose_name = _(u'Content')
        verbose_name_plural = _(u'Content')

    def __str__(self):
        return self.title

    def allow_comment(self):
        return self.comments

    @property
    def hash(self):
        return id_to_hash(self.id, length=self.HASH_LENGTH)

    @property
    def parent(self):
        return 1

    @property
    def short_content(self):
        return self.content.split(cutter, 1)[0]

    @property
    def long_content(self):
        return self.content.split(cutter, 1)[1]

    def get_upload_path(self, filename):
        return 'content/%s/%s' % (datetime.now().strftime("%Y/%m"), filename)

    def __unique_slug(self, slug, my_id, counter=1):
        counter += 1
        gen_slug = "%s-%s" % (slug, counter)
        exists = self._default_manager.filter(slug=gen_slug).exclude(id=my_id)
        if exists:
            return self.__unique_slug(slug, my_id, counter)
        else:
            return gen_slug

    def update_url(self):
        url = self.slug
        parent = self.get_parent(update=True)
        if parent:
            url = "%s/%s" % (parent.url, self.slug)

        if self.url != url:
            Content.objects.filter(id=self.pk).update(url=url)

            children = self.get_children()
            for child in children:
                child.update_url()

    def save(self, *args, **kwargs):
        update_slug = False
        if self.pk is not None:
            old = Content.objects.get(pk=self.pk)
            if old.slug != self.slug:
                update_slug = True
        else:
            update_slug = True

        if update_slug is True:
            self.slug = unique_slug(
                Content, 'slug', self.slug, query={'type': self.type}
                # Content, 'slug', self.slug, query={'parent': self.parent, 'type': self.type}
            )

        super(Content, self).save(*args, **kwargs)
        if update_slug is True:
            self.update_url()


class Snippet(models.Model):
    slug = models.SlugField(verbose_name=_(u'Slug'), max_length=255, db_index=True)
    title = models.CharField(_(u'Title'), max_length=255, default='')
    content = RichTextField(_(u'Content'), blank=True)

    class Meta:
        verbose_name = _(u'Snippet')
        verbose_name_plural = _(u'Snippet')

    def __unicode__(self):
        return self.title

    def __unique_slug(self, slug, my_id, counter=1):
        counter += 1
        gen_slug = "%s-%s" % (slug, counter)
        exists = self._default_manager.filter(slug=gen_slug).exclude(id=my_id)
        if exists:
            return self.__unique_slug(slug, my_id, counter)
        else:
            return gen_slug
