# -*- coding: utf-8 -*-

import requests

from chikyu_sdk.api_resource import ApiResource


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

        url = cls._build_url("open", path)
        resp = requests.post(
            url,
            json=params,
            headers={'content-type': 'application/json'})

        return cls._handle_response(path, resp)
