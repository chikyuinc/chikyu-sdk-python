# -*- coding: utf-8 -*-
"""
SFA Open Resource
認証なしで呼ばれるSFA API用（セッショントークン作成など）
"""

import requests

from chikyu_sdk.api_resource import ApiResource
from chikyu_sdk.error.common_errors import HttpException, ApiExecuteException


class SfaOpenResource(ApiResource):
    @classmethod
    def _handle_sfa_response(cls, path, resp):
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

    @classmethod
    def invoke(cls, path, data, method='POST'):
        """
        SFA Open APIを呼び出す

        :param path: APIのパス (例: 'SessionToken.create')
        :param data: APIに渡すデータ
        :param method: HTTPメソッド (デフォルト: POST)
        :rtype: dict
        :return: APIレスポンス
        """
        url = cls._build_url("sfa_open", path)
        headers = {'content-type': 'application/json'}

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

        return cls._handle_sfa_response(path, resp)

