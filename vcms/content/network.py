# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

import os
import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

from logging import getLogger
log = getLogger(__file__)


class Download:
    def __init__(self, *args, **kwargs):
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'
        self.referer = None
        self.accept_lang = 'en-US,en;q=0.5'
        self.min_length = 0
        self.max_length = 1024*1024*10

        self.s = requests.Session()
        retries = Retry(total=5,
                        redirect=5,
                        backoff_factor=0.1,
                        status_forcelist=[500, 502, 503, 504])

        self.s.mount('http://', HTTPAdapter(max_retries=retries))
        self.s.mount('https://', HTTPAdapter(max_retries=retries))

    def headers(self):
        h = {
            'User-Agent': self.user_agent,
            'Accept-Language': self.accept_lang,
        }
        if self.referer:
            h['Referer'] = self.referer

    def get(self, url):
        res = self.s.get(url, headers=self.headers())
        res.status_code

    def post(self, url, params={}):
        res = self.s.post(url, data=params, headers=self.headers())

    def download(self, url, target):
        res = self.s.get(url, headers=self.headers(), stream=True)
        log.debug(res.status_code)
        log.debug(res.history)

        if res.status_code != 200:
            log.error(res.status_code)
            return False

        if os.path.exists(os.path.dirname(target)) is False:
            os.makedirs(os.path.dirname(target), exist_ok=True)

        if self.min_length < int(res.headers['content-length']) < self.max_length:
            with open(target, 'wb') as f:
                f.write(res.content)

        del res
        return target
