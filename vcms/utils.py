# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'


def unique_slug(instance, slug_field, slug, counter=0, query=None):
    if counter > 0:
        test_slug = "%s_%s" % (slug, counter)
    else:
        test_slug = slug

    rs = instance.objects.filter(**{slug_field: test_slug})
    if query:
        rs = rs.filter(**query)
    if rs[:1]:
        counter += 1
        return unique_slug(instance, slug_field, slug, counter, query)
    else:
        return test_slug
