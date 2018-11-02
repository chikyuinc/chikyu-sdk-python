# -*- coding: utf-8 -*-

import json
import six

from decimal import Decimal


"""
JSONに関連するヘルパーモジュールです
"""


def to_str(s):
    if six.PY2:
        if isinstance(s, str):
            return s.decode('utf-8')
        elif isinstance(s, unicode):
            return s
        else:
            return str(s).decode('utf-8')
    else:
        return str(s)


def __to_unicode(_v, all_to_unicode=False):
    if _v is None:
        return None

    if isinstance(_v, dict):
        return to_unicode_dict(_v, all_to_unicode)
    if isinstance(_v, list) or isinstance(_v, tuple):
        return to_unicode_list(_v, all_to_unicode)
    else:
        if all_to_unicode:
            if isinstance(_v, float) or isinstance(_v, int) or isinstance(_v, bool):
                return _v
            elif isinstance(_v, Decimal):
                return float(_v)
            elif isinstance(_v, six.string_types):
                return to_str(_v)
            else:
                return _v
        else:
            return _v


def to_unicode_list(obj, all_to_unicode=True):
    """

    listオブジェクトを走査し、JSONに変換可能なデータ型に変換します

    :param obj:
    :param all_to_unicode:
    :return:
    """
    return list(map(lambda v: __to_unicode(v, all_to_unicode), obj))


def to_unicode_dict(obj, all_to_unicode=True):
    """

    dictオブジェクトを走査し、JSONに変換可能なデータ型に変換します

    :param obj:
    :param all_to_unicode:
    :return:
    """
    return dict(map(lambda v: (v[0], __to_unicode(v[1], all_to_unicode)), obj.items()))


def to_unicode_all(obj, all_to_unicode=True):
    """

    指定したオブジェクトを走査し、JSONに変換可能なデータ型に変換します

    :param obj:
    :param all_to_unicode:
    :return:
    """
    if obj is None:
        return None
    elif isinstance(obj, dict):
        return to_unicode_dict(obj, all_to_unicode)
    elif isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, set):
        return to_unicode_list(obj, all_to_unicode)
    else:
        return to_str(obj)


def to_json(obj, to_unicode=True):
    """

    オブジェクトをJSONに変換します(通常はこのメソッドだけを用いれば問題ありません)

    :param obj:
    :param to_unicode:
    :return:
    """

    if to_unicode:
        converted = to_unicode_all(obj, True)
        return json.dumps(converted)
    else:
        return json.dumps(obj)


def from_json(s):
    """

    JSONからオブジェクトに変換します

    :param s:
    :return:
    """
    return json.loads(s)


def format_as_json(obj):
    """

    printした際に見やすいよう、フォーマットされた文字列としてオブジェクトをJSONに変換します

    :param obj:
    :return:
    """
    return json.dumps(to_unicode_all(obj), indent=4, separators=(',', ': '), ensure_ascii=False)
