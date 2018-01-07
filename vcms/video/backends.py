# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

import re
from embed_video.backends import VideoBackend


class RedTube(VideoBackend):
    re_detect = re.compile(r'https://www\.redtube\.com/[0-9]+')
    re_code = re.compile(r'https://www\.redtube\.com/(?P<code>[0-9]+)')

    allow_https = True
    pattern_url = '{protocol}://embed.redtube.com/?id={code}&bgcolor=000000'

