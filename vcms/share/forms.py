# -*- coding: utf-8 -*-
__author__ = 'Vadim'

from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from vcms.share.models import Share


class AddSnippetForm(forms.ModelForm):
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

    type = forms.ChoiceField(choices=PYGMENTS_CHOISE)

    def __init__(self, *args, **kwargs):
        super(AddSnippetForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Share
        exclude = ['user', 'time_created', 'time_updated', 'views', 'disabled', 'slug', 'file_name', 'json']

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
