# -*- coding: utf-8 -*-
import pytest
import os.path
from ConfigParser import SafeConfigParser

from logging import basicConfig
basicConfig()


def get_test_config():
    config_path = "{}/config.ini".format(os.path.dirname(__file__))
    if os.path.exists(config_path):
        conf = SafeConfigParser()
        conf.read(config_path)
        return conf
    else:
        raise RuntimeError("設定ファイルが見つかりません: {}".format(config_path))


configs = get_test_config()
