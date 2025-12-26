# -*- coding: utf-8 -*-
"""
SFA Public Resource
APIキー認証で呼ばれるSFA API用（外部公開API）
"""

import requests

from chikyu_sdk.api_resource import ApiResource
from chikyu_sdk.error.common_errors import HttpException, ApiExecuteException


class SfaPublicResource(ApiResource):
    def __init__(self, api_key, auth_key):
        """
        :param api_key: APIキー
        :param auth_key: 認証キー
        """
        super(SfaPublicResource, self).__init__()
        self.__api_key = api_key
        self.__auth_key = auth_key

    def _handle_sfa_response(self, path, resp):
        """
        SFA APIのレスポンスをハンドリング
        新しいSFA APIはsuccessフィールドを使用
        レスポンス全体（success, payload, error_list等）を返す
        """
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
        SFA Public APIを呼び出す

        :param path: APIのパス (例: 'ObjectRecords.create')
        :param data: APIに渡すデータ
        :param method: HTTPメソッド (デフォルト: POST)
        :rtype: dict
        :return: APIレスポンス
        """
        url = self._build_url("sfa_public", path)
        headers = {
            'content-type': 'application/json',
            'x-api-key': self.__api_key,
            'x-auth-key': self.__auth_key
        }

        if method.upper() == 'GET':
            resp = requests.get(url, headers=headers)
        elif method.upper() == 'POST':
            resp = requests.post(url, json=data, headers=headers)
        elif method.upper() == 'PUT':
            resp = requests.put(url, json=data, headers=headers)
        elif method.upper() == 'DELETE':
            resp = requests.delete(url, json=data, headers=headers)
        else:
            resp = requests.post(url, json=data, headers=headers)

        return self._handle_sfa_response(path, resp)

    def get(self, path):
        """
        SFA Public API GET

        :param path: APIのパス
        :rtype: dict
        """
        return self.invoke(path, method='GET')

    def post(self, path, data):
        """
        SFA Public API POST

        :param path: APIのパス
        :param data: APIに渡すデータ
        :rtype: dict
        """
        return self.invoke(path, data, method='POST')

    def put(self, path, data):
        """
        SFA Public API PUT

        :param path: APIのパス
        :param data: APIに渡すデータ
        :rtype: dict
        """
        return self.invoke(path, data, method='PUT')

    def delete(self, path, data=None):
        """
        SFA Public API DELETE

        :param path: APIのパス
        :param data: APIに渡すデータ (オプション)
        :rtype: dict
        """
        return self.invoke(path, data, method='DELETE')

