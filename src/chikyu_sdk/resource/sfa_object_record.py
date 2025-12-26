# -*- coding: utf-8 -*-
"""
SFA ObjectRecord Resource
SFA Public API経由でObjectRecordsを操作するためのリソースクラス
"""

from chikyu_sdk.sfa_public_resource import SfaPublicResource


class SfaObjectRecord(object):
    """SFA Public API経由でObjectRecordsを操作するリソースクラス。

    使用例:
        from chikyu_sdk.resource.sfa_object_record import SfaObjectRecord

        obj_record = SfaObjectRecord('api_key', 'auth_key')

        # レコード単体取得
        result = obj_record.single('companies', '5abc123def456')

        # レコード削除
        result = obj_record.delete('companies', '5abc123def456')

        # レコード件数カウント
        result = obj_record.count('prospects')

        # 集計
        result = obj_record.aggregate('opportunities', group_by=['status'], aggregates=[...])

        # クロス検索
        result = obj_record.cross_search('検索テキスト')
    """

    def __init__(self, api_key, auth_key):
        """
        :param api_key: APIキー
        :param auth_key: 認証キー
        """
        self._resource = SfaPublicResource(api_key, auth_key)

    def single(self, collection_name, record_id, fields=None):
        """レコードを単体取得する。

        :param collection_name: コレクション名（例: 'prospects', 'companies'）
        :param record_id: 取得するレコードのID
        :param fields: 取得するフィールドのリスト（任意）。指定しない場合は全フィールドを取得
        :rtype: dict
        :return: APIレスポンス（success, payload等を含む）
        """
        data = {
            'collection_name': collection_name,
            'key': record_id
        }
        if fields:
            data['fields'] = fields

        return self._resource.post('ObjectRecords.single', data)

    def delete(self, collection_name, record_id):
        """レコードを削除する。

        :param collection_name: コレクション名（例: 'prospects', 'companies'）
        :param record_id: 削除するレコードのID
        :rtype: dict
        :return: APIレスポンス（success, payload等を含む）
        """
        data = {
            'collection_name': collection_name,
            'record_id': record_id
        }
        return self._resource.post('ObjectRecords.delete', data)

    def count(self, object_name, where=None, list_id=None):
        """レコード件数をカウントする。

        :param object_name: オブジェクトパス（例: 'Organizations/7223/Objects/companies'）
        :param where: 絞り込み条件（任意）
        :param list_id: 絞り込みリストのID（任意）
        :rtype: dict
        :return: APIレスポンス（success, payload等を含む）
        """
        data = {
            'object_name': object_name,
            'where': where,  # 必須フィールド（nullも可）
            'list_id': list_id  # 必須フィールド（nullも可）
        }

        return self._resource.post('ObjectRecords.count', data)

    def aggregate(self, object_name, group_list, target_list, where=None, list_id=None):
        """レコードを集計する。

        :param object_name: オブジェクトパス（例: 'Organizations/7223/Objects/companies'）
        :param group_list: グループ条件リスト
                          例: [{'field_name': 'status', 'grouping_type': 'normal'}]
                          grouping_type: 日付型は year/quarter/month/week/day/hour/minute, その他は normal
        :param target_list: 集計対象リスト
                           例: [{'field_name': 'amount', 'aggregation_type': 'sum'}]
                           件数カウント: [{'field_name': '__count__', 'aggregation_type': 'sum'}]
                           aggregation_type: sum, avg, min, max
        :param where: 絞り込み条件（任意）
        :param list_id: 検索に利用するリストのID（任意）
        :rtype: dict
        :return: APIレスポンス（success, payload等を含む）
        """
        data = {
            'object_name': object_name,
            'group_list': group_list,
            'target_list': target_list,
            'where': where,  # 必須フィールド（nullも可）
            'list_id': list_id  # 必須フィールド（nullも可）
        }

        return self._resource.post('ObjectRecords.aggregate', data)

    def cross_search(self, keyword, target_collection_names, items_per_page=10, page_index=0, ignore_fields=None):
        """クロス検索（複数オブジェクト横断検索）を実行する。

        :param keyword: 検索キーワード
        :param target_collection_names: 検索対象のコレクション名のリスト
        :param items_per_page: 1ページあたりの件数（デフォルト: 10）
        :param page_index: ページインデックス（デフォルト: 0）
        :param ignore_fields: 無視するフィールド名のリスト（任意）
        :rtype: dict
        :return: APIレスポンス（success, payload等を含む）
        """
        data = {
            'keyword': keyword,
            'target_collection_names': target_collection_names,
            'items_per_page': items_per_page,
            'page_index': page_index,
            'ignore_fields': ignore_fields or []
        }

        return self._resource.post('ObjectRecords.cross_search', data)

