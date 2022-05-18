# -*- coding: utf-8 -*-

import requests
from logging import getLogger

from chikyu_sdk.helper import file_helper

__logger = getLogger(__name__)


def get(url, payload=None, headers=None):
    if headers:
        if not payload:
            res = requests.get(url, headers=headers)
        else:
            res = requests.get(url, payload=payload, headers=headers)
    else:
        if not payload:
            res = requests.get(url)
        else:
            res = requests.get(url, payload=payload)

    if res.status_code == 200:
        return res.content
    else:
        __logger.error('request send error:{} / {}'.format(url, payload))
        return None


def put_file(url, file_path, content_type, as_binary=True):
    hd = dict()
    hd['content-type'] = content_type

    file_data = file_helper.read_file(file_path, as_binary)
    if not file_data:
        return False
    r = requests.put(url, data=file_data, headers=hd)
    if r.status_code == 200:
        return True
    else:
        __logger.error("status={} | content={}".format(r.status_code, r.content))
        return False


def get_file(url, file_path):
    content = get(url)
    file_helper.write_file(file_path, content)
