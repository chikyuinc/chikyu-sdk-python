# -*- coding: utf-8 -*-
import six
from chikyu_sdk.config.api_config import ApiConfig
from chikyu_sdk.error.common_errors import HttpException, ApiExecuteException
from logging import getLogger

from chikyu_sdk.helper.json_helper import to_str, to_unicode_all


class ApiResource(object):
    _logger = getLogger(__name__)

    @classmethod
    def _build_url(cls, api_class, api_path, with_host=True):
        if with_host:
            url = "{}://{}".format(ApiConfig.protocol(), ApiConfig.host())
        else:
            url = ""

        if api_path.startswith('/'):
            p = api_path[1:]
        else:
            p = api_path

        env_name = ApiConfig.env_name()
        if env_name:
            url = "{}/{}/api/v2/{}/{}".format(url, env_name, api_class, p)
        else:
            url = "{}/api/v2/{}/{}".format(url, api_class, p)
        cls._logger.debug(url)
        return url

    @classmethod
    def _handle_response(cls, path, resp):
        use_http_status = ApiConfig.use_http_status()
        http_status = resp.status_code

        if use_http_status:
            allowed_status_codes = [200, 400]
        else:
            allowed_status_codes = [200]

        if http_status not in allowed_status_codes:
            try:
                item = resp.json()
                if 'message' in item:
                    err_msg = item['message']
                else:
                    err_msg = ''
            except:
                err_msg = resp.content

            if six.PY2:
                msg = u"httpエラーが発生しました -> url={} / status={} / message={}".format(
                    to_str(path), to_str(http_status), to_str(err_msg))
            else:
                msg = \
                    u"httpエラーが発生しました -> url={} / status={} / message={}".format(path, http_status, err_msg)
            cls._logger.error(msg)
            raise HttpException(msg, http_status=http_status)

        content = resp.json()
        if content['has_error']:
            if 'message' in content:
                if six.PY2:
                    msg = \
                        u"APIの実行に失敗しました -> url={} / message={}".format(to_str(path), to_str(content['message']))
                else:
                    msg = "APIの実行に失敗しました -> url={} / message={}".format(path, content['message'])
            else:
                msg = "APIの実行に失敗しました"
            cls._logger.error(msg)
            raise ApiExecuteException(msg, http_status=http_status)

        if 'data' in content:
            return to_unicode_all(content['data'])


class ApiObject(object):
    pass
