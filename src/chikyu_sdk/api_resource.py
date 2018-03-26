# -*- coding: utf-8 -*-
from chikyu_sdk.config.api_config import ApiConfig
from chikyu_sdk.error.common_errors import HttpException, ApiExecuteException
from logging import getLogger


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
        if resp.status_code != 200:
            try:
                item = resp.json()
                if 'message' in item:
                    err_msg = item['message']
                else:
                    err_msg = ''
            except:
                err_msg = resp.content

            msg = u"httpエラーが発生しました -> url={} / status={} / message={}".format(path, resp.status_code, err_msg)
            cls._logger.error(msg)
            raise HttpException(msg)

        content = resp.json()
        if content['has_error']:
            if 'message' in content:
                msg = u"APIの実行に失敗しました -> url={} / message={}".format(path, content['message'])
            else:
                msg = u"APIの実行に失敗しました"
            cls._logger.error(msg)
            raise ApiExecuteException(msg)

        if 'data' in content:
            return content['data']


class ApiObject(object):
    pass
