# -*- coding: utf-8 -*-
import pytest
import os.path
from chikyu_sdk.config.api_config import ApiConfig
from ConfigParser import SafeConfigParser

from logging import basicConfig
basicConfig()


ApiConfig.set_mode('local')


def get_test_config():
    config_path = "{}/config.{}.ini".format(os.path.dirname(__file__), ApiConfig.mode())
    if os.path.exists(config_path):
        conf = SafeConfigParser()
        conf.read(config_path)
        return conf
    else:
        raise RuntimeError("設定ファイルが見つかりません: {}".format(config_path))


configs = get_test_config()
