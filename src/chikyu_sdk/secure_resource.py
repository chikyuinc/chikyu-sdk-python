# -*- coding: utf-8 -*-

import requests
from requests_aws4auth import AWS4Auth

from chikyu_sdk.api_resource import ApiResource
from chikyu_sdk.config import configs


class SecureResource(ApiResource):
    def __init__(self, session):
        """
        :param session: chikyu_sdk.resource.session.Session
        """
        super(SecureResource, self).__init__()
        self.__session = session

        self.__auth = AWS4Auth(self.__session.credentials.key_id,
                               self.__session.credentials.secret_key,
                               configs.AWS_REGION,
                               configs.AWS_API_GW_SERVICE_NAME,
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

        if configs.IS_LOCAL:
            params['identity_id'] = self.__session.identity_id
            params['identity_pool_id'] = configs.AWS_COGNITO_IDENTITY_POOL_ID

        res = requests.post(
            url=url,
            json=params,
            headers={'x-api-key': self.__session.api_key, 'content-type': 'application/json'},
            auth=self.__auth
        )

        return self._handle_response(path, res)
