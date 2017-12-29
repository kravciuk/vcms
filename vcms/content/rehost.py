# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

import requests
import re
import os
import uuid
from datetime import datetime
from lxml import html
from urllib.parse import urlparse, urljoin
from .network import Download

from django.conf import settings

import logging as log

class Rehost:

    def __init__(self):
        self.url = None
        self.no_to_download = 0
        self.format_list = ["jpg", "png", "gif", "svg", "jpeg"]
        self.download_path = "images"
        self.min_filesize = 0
        self.max_filesize = 100000000
        self.dump_urls = False
        self.scrape_reverse = False
        self.use_ghost = False
        self.images = None
        self.nthreads = 10
        self.filename_pattern = None
        self.page_html = None
        self.page_url = None
        self.proxy_url = None
        self.proxies = {}

    @staticmethod
    def ext(name):
        return os.path.splitext(name)[1].lower()

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
        for image in r.get_img_list():
            path = os.path.join('rehost', Rehost.today(), "%s.%s" % (uuid.uuid4(), Rehost.ext(image)))
            d.download(image, os.path.join(settings.MEDIA_ROOT, path))
            html = html.replace(image, "/media/%s" % path)
        del d
        del r
        return html

    def get_img_list(self):
        log.debug('Extracting images')
        """ Gets list of images from the page_html. """
        tree = html.fromstring(self.page_html)
        img = tree.xpath('//img/@src')
        links = tree.xpath('//a/@href')
        img_list = self.process_links(img)
        img_links = self.process_links(links)
        img_list.extend(img_links)

        if self.filename_pattern:
            # Compile pattern for efficiency
            pattern = re.compile(self.filename_pattern)

            # Verifies filename in the image URL matches pattern
            def matches_pattern(img_url):
                """ Function to check if pattern is matched. """

                img_filename = urlparse(img_url).path.split('/')[-1]
                return pattern.search(img_filename)

            images = [urljoin(self.url, img_url) for img_url in img_list
                      if matches_pattern(img_url)]
        else:
            images = [urljoin(self.url, img_url) for img_url in img_list]

        images = list(set(images))
        self.images = images
        if self.scrape_reverse:
            self.images.reverse()
        return self.images

    def download_image(self, img_url):
        """ Downloads a single image.
            Downloads img_url using self.page_url as base.
            Also, raises the appropriate exception if required.
        """
        img_request = None
        try:
            img_request = requests.request(
                'get', img_url, stream=True, proxies=self.proxies, allow_redirects=True)
            if img_request.status_code != 200:
                log.error(img_request.status_code)
                return
        except:
            log.error('Dewnload error')
            return

        if img_url[-3:] == "svg" or (int(img_request.headers['content-length']) > self.min_filesize and\
                                     int(img_request.headers['content-length']) < self.max_filesize):
            img_content = img_request.content
            with open(os.path.join(self.download_path, img_url.split('/')[-1]), 'wb') as f:
                byte_image = bytes(img_content)
                f.write(byte_image)
        else:
            log.error(img_request.headers['content-length'])
            return
        return True

    def process_links(self, links):
        """ Function to process the list of links and filter required links."""
        links_list = []
        for link in links:
            if os.path.splitext(link)[1][1:].strip().lower() in self.format_list:
                links_list.append(link)
        return links_list
