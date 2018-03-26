# -*- coding: utf-8 -*-

import requests
from requests_aws4auth import AWS4Auth

from chikyu_sdk.api_resource import ApiResource
from chikyu_sdk.config.api_config import ApiConfig


class SecureResource(ApiResource):
    def __init__(self, session):
        """
        :param session: chikyu_sdk.resource.session.Session
        """
        super(SecureResource, self).__init__()
        self.__session = session

        self.__auth = AWS4Auth(self.__session.credentials.key_id,
                               self.__session.credentials.secret_key,
                               ApiConfig.aws_region(),
                               ApiConfig.aws_api_gw_service_name(),
                               session_token=self.__session.credentials.session_token)

    def invoke(self, path, data):
        """
        :param path: APIのパス
        :param data: APIに渡すデータ(リクエストのプロパティである「data」に入るもの)
        :rtype: dict
        :return:
        """
        url = self._build_url("secure", path)
        params = {'session_id': self.__session.session_id, 'data': data}

        if ApiConfig.mode() == "local":
            params['identity_id'] = self.__session.identity_id

        res = requests.post(
            url=url,
            json=params,
            headers={'x-api-key': self.__session.api_key, 'content-type': 'application/json'},
            auth=self.__auth
        )

        return self._handle_response(path, res)
