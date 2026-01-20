# -*- coding: utf-8 -*-
"""
SFA Secure Resource
セッション認証で呼ばれるSFA API用
GET, POST, PUT, DELETE メソッドをサポート
"""

import requests
from requests_aws4auth import AWS4Auth

from chikyu_sdk.api_resource import ApiResource
from chikyu_sdk.config.api_config import ApiConfig
from chikyu_sdk.error.common_errors import HttpException, ApiExecuteException


class SfaSecureResource(ApiResource):
    def __init__(self, session):
        """
        :param session: chikyu_sdk.resource.session.Session
        """
        super(SfaSecureResource, self).__init__()
        self.__session = session

        self.__auth = AWS4Auth(
            self.__session.credentials.key_id,
            self.__session.credentials.secret_key,
            ApiConfig.aws_region(),
            ApiConfig.aws_api_gw_service_name(),
            session_token=self.__session.credentials.session_token
        )

    def _build_headers(self):
        """SFA Secure API用のヘッダーを構築"""
        headers = {
            'content-type': 'application/json',
            'x-api-key': self.__session.api_key,
            'x-session-id': self.__session.session_id,
            'x-identity-id': self.__session.identity_id
        }
        return headers

    def _handle_sfa_response(self, path, resp):
        """
        SFA APIのレスポンスをハンドリング
        新しいSFA APIはsuccessフィールドを使用
        レスポンス全体（success, payload, error_list等）を返す
        Lambda Proxy形式のレスポンスにも対応
        """
        import json as json_module

        if resp.status_code != 200:
            try:
                item = resp.json()
                err_msg = item.get('message', item.get('detail', ''))
            except Exception:
                err_msg = resp.content
            msg = u"httpエラーが発生しました -> url={} / status={} / message={}".format(
                path, resp.status_code, err_msg)
            raise HttpException(msg)

        content = resp.json()

        # Lambda Proxy形式のレスポンスを検出して変換
        # ローカル開発環境（server.py）からのレスポンスがこの形式になる場合がある
        if 'statusCode' in content and 'body' in content and 'isBase64Encoded' in content:
            status_code = content.get('statusCode', 200)
            body_str = content.get('body', '{}')
            try:
                content = json_module.loads(body_str)
            except (json_module.JSONDecodeError, TypeError):
                content = {'message': body_str}

            # Lambda Proxy形式でエラーステータスの場合
            if status_code != 200:
                error_list = content.get('error_list', [])
                if error_list:
                    err_msg = error_list[0].get('message', 'APIの実行に失敗しました')
                else:
                    err_msg = content.get('message', content.get('detail', 'APIの実行に失敗しました'))
                msg = u"httpエラーが発生しました -> url={} / status={} / message={}".format(
                    path, status_code, err_msg)
                raise HttpException(msg)

        # 新しいSFA API形式: successフィールドを使用
        if 'success' in content:
            if not content['success']:
                error_list = content.get('error_list', [])
                if error_list:
                    msg = error_list[0].get('message', 'APIの実行に失敗しました')
                else:
                    msg = content.get('message', 'APIの実行に失敗しました')
                raise ApiExecuteException(msg)
            # レスポンス全体を返す（payload抽出ではなく）
            return content

        # 既存API形式にフォールバック: has_errorフィールドを使用
        if 'has_error' in content:
            if content['has_error']:
                msg = content.get('message', 'APIの実行に失敗しました')
                raise ApiExecuteException(msg)
            # レスポンス全体を返す（data抽出ではなく）
            return content

        # どちらでもない場合はそのまま返す
        return content

    def invoke(self, path, data=None, method='POST'):
        """
        SFA Secure APIを呼び出す (POST)

        :param path: APIのパス (例: 'SystemApiAuthKeys')
        :param data: APIに渡すデータ
        :param method: HTTPメソッド
        :rtype: dict
        :return: APIレスポンス
        """
        url = self._build_url("sfa_secure", path)
        headers = self._build_headers()

        if method.upper() == 'GET':
            resp = requests.get(url, headers=headers, auth=self.__auth)
        elif method.upper() == 'POST':
            resp = requests.post(url, json=data, headers=headers, auth=self.__auth)
        elif method.upper() == 'PUT':
            resp = requests.put(url, json=data, headers=headers, auth=self.__auth)
        elif method.upper() == 'DELETE':
            resp = requests.delete(url, json=data, headers=headers, auth=self.__auth)
        else:
            resp = requests.post(url, json=data, headers=headers, auth=self.__auth)

        return self._handle_sfa_response(path, resp)

    def get(self, path):
        """
        SFA Secure API GET

        :param path: APIのパス
        :rtype: dict
        """
        return self.invoke(path, method='GET')

    def post(self, path, data):
        """
        SFA Secure API POST

        :param path: APIのパス
        :param data: APIに渡すデータ
        :rtype: dict
        """
        return self.invoke(path, data, method='POST')

    def put(self, path, data):
        """
        SFA Secure API PUT

        :param path: APIのパス
        :param data: APIに渡すデータ
        :rtype: dict
        """
        return self.invoke(path, data, method='PUT')

    def delete(self, path, data=None):
        """
        SFA Secure API DELETE

        :param path: APIのパス
        :param data: APIに渡すデータ (オプション)
        :rtype: dict
        """
        return self.invoke(path, data, method='DELETE')

