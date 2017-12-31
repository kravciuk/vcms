# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

from django import forms
from vcms.content.models import Content
from django_select2.forms import Select2Widget, HeavySelect2Widget, ModelSelect2Widget
from treebeard.forms import MoveNodeForm, movenodeform_factory


class MyWidget(Select2Widget):
    search_fields = [
        'title__icontains', 'url__icontains'
    ]

    def get_queryset(self):
        """
        Return QuerySet based on :attr:`.queryset` or :attr:`.model`.

        Returns:
            QuerySet: QuerySet of available choices.

        """
        if self.queryset is not None:
            queryset = self.queryset
        elif self.model is not None:
            queryset = self.model._default_manager.all()
        else:
            raise NotImplementedError(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {
                    'cls': self.__class__.__name__
                }
            )
        return queryset.filter(type__in=[Content.TYPE_PAGE])


class PageContentForm(forms.ModelForm):
    after = forms.CharField(widget=forms.HiddenInput(), required=False)
    page = forms.CharField(widget=forms.HiddenInput(), required=False)
    rehost = forms.BooleanField(required=False, initial=False)

    def __init__(self, *args, **kwargs):
        super(PageContentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Content
        exclude = ['show_count', 'view_count', 'custom', 'user', 'rating', 'type', 'id']

    def full_clean(self):
        super(PageContentForm, self).full_clean()

        if 'numchild' in self._errors:
            del self._errors['numchild']

        if 'depth' in self._errors:
            del self._errors['depth']

        if 'path' in self._errors:
            del self._errors['path']

