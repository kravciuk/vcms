# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

import requests
import re
import os
import uuid
from datetime import datetime
from lxml import html
from urllib.parse import urlparse, urljoin
from vu.network import Download
from vu.threads import ThreadPool
from django.conf import settings

import logging as log


class Rehost:

    def __init__(self):
        self.url = None
        self.format_list = ["jpg", "png", "gif", "svg", "jpeg"]
        self.download_path = "images"
        self.min_filesize = 0
        self.max_filesize = 100000000
        self.page_html = None

    @staticmethod
    def ext(name):
        return os.path.splitext(name)[1].lower()[1:]

    @staticmethod
    def file_name(name):
        return os.path.basename(name)

    @staticmethod
    def today():
        return datetime.today().strftime("%Y/%m/%d")

    @staticmethod
    def images(html):
        d = Download()
        r = Rehost()
        r.page_html = html
        pool = ThreadPool(3)
        for image in r.get_img_list():
            path = os.path.join('rehost', Rehost.today(), "%s.%s" % (uuid.uuid4(), Rehost.ext(image)))
            # d.download(image, os.path.join(settings.MEDIA_ROOT, path))
            pool.add_task(d.download, image, os.path.join(settings.MEDIA_ROOT, path))
            html = html.replace(image, "/media/%s" % path)
        pool.wait_completion()
        del d
        del r
        return html

    def get_img_list(self):
        tree = html.fromstring(self.page_html)
        img = tree.xpath('//img/@src')
        links = tree.xpath('//a/@href')
        img_list = self.process_links(img)
        img_links = self.process_links(links)
        img_list.extend(img_links)

        images = [urljoin(self.url, img_url) for img_url in img_list]
        return list(set(images))

    def process_links(self, links):
        links_list = []
        for link in links:
            if Rehost.ext(link).lower() in self.format_list:
                links_list.append(link)
        return links_list
