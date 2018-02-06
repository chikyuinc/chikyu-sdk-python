# -*- coding: utf-8 -*-

import requests

from chikyu_sdk.api_resource import ApiResource


class PublicResource(ApiResource):
    def __init__(self, api_key, auth_key):
        """
        :param api_key:
        :param auth_key:
        """
        super(PublicResource, self).__init__()
        self.__api_key = api_key
        self.__auth_key = auth_key

    def invoke(self, path, data):
        """
        :param path: APIのパス
        :param data: APIに渡すデータ(リクエストのプロパティである「data」に入るもの)
        :rtype: dict
        :return:
        """
        params = {'data': data}

        url = self._build_url("public", path)
        resp = requests.post(
            url,
            json=params,
            headers={'content-type': 'application/json',
                     'x-api-key': self.__api_key,
                     'x-auth-key': self.__auth_key})

        return self._handle_response(path, resp)
