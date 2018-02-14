# -*- coding: utf-8 -*-

from os import path
from logging import getLogger
__logger = getLogger(__name__)


def read_file(file_path, as_binary=False):
    if file_path is None:
        return None

    if not path.exists(file_path):
        __logger.error('{file_name} not exists'.format(file_name=file_path))
        return None

    if as_binary:
        fh = open(file_path, 'rb')
    else:
        fh = open(file_path)
    try:
        return fh.read()
    finally:
        fh.close()


def write_file(file_path, content, as_binary=True):
    if file_path is None or content is None:
        return None

    if as_binary:
        fh = open(file_path, 'wb')
    else:
        fh = open(file_path, 'w')
    try:
        fh.write(content)
    finally:
        fh.close()
