# -*- coding: utf-8 -*-


class HttpException(Exception):
    """HTTP通信エラーを表す例外クラス。

    :param message: エラーメッセージ
    :param http_status: HTTPステータスコード
    """
    def __init__(self, message, http_status=None):
        super(HttpException, self).__init__(message)
        self.http_status = http_status


class ApiExecuteException(Exception):
    """API実行エラーを表す例外クラス。

    :param message: エラーメッセージ
    :param http_status: HTTPステータスコード
    """
    def __init__(self, message, http_status=None):
        super(ApiExecuteException, self).__init__(message)
        self.http_status = http_status
