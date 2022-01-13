# -*- coding: utf-8 -*-
__author__ = 'Vadim'

from django import forms

from pygments.lexers import get_all_lexers

from django.contrib.admin.widgets import AdminDateWidget
from vcms.share.models import Share, Pygment



class AddSnippetForm(forms.ModelForm):
    file = forms.FileField(required=False)
    delete_file = forms.MultipleChoiceField(required=False, widget = forms.CheckboxSelectMultiple())

    def __init__(self, *args, **kwargs):
        super(AddSnippetForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Share
        exclude = ['user', 'time_created', 'time_updated', 'views', 'disabled', 'slug', 'file', 'json']

    class Media:
        css = {
            'all': ('datepicker/datepicker.css',)
        }
        js = [
            'datepicker/datepicker.js',
        ]

    def clean(self):
        cleaned_data = super(AddSnippetForm, self).clean()

        content = (cleaned_data.get('content') or '').strip()
        url = (cleaned_data.get('url') or '').strip()
        description = (cleaned_data.get('description') or '').strip()

        if not content and not description and not url and 'file' not in self.files:
            raise forms.ValidationError('Please upload a image or add content text.')

        return cleaned_data


class FileUploadForm(forms.Form):
    file = forms.FileField()


class AdminPygmentForm(forms.ModelForm):
    code = forms.ChoiceField()
    model = Pygment

    def __init__(self, *args, **kwargs):
        choice = []
        for lexer in get_all_lexers():
            if lexer[1]:
                choice.append((lexer[1][0], lexer[0]))
        super().__init__(*args, **kwargs)
        self.fields['code'].choices = choice