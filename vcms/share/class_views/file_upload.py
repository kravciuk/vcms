# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'
from django.views.generic.edit import FormView
from share.forms import FileUploadForm


class FileUploadView(FormView):
    form_class = FileUploadForm

    def form_valid(self, form):
        self.request
        return
