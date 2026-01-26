# -*- coding: utf-8 -*-

import requests

from chikyu_sdk.api_resource import ApiResource
from chikyu_sdk.config.api_config import ApiConfig


class OpenResource(ApiResource):
    @classmethod
    def invoke(cls, path, data):
        """
        :param path: APIのパス
        :param data: APIに渡すデータ(リクエストのプロパティである「data」に入るもの)
        :rtype: dict
        :return:
        """
        params = {'data': data}

        headers = {'content-type': 'application/json'}
        if ApiConfig.use_http_status():
            headers['Error-Response'] = 'http-status'

        url = cls._build_url("open", path)
        resp = requests.post(
            url,
            json=params,
            headers=headers)

        return cls._handle_response(path, resp)
