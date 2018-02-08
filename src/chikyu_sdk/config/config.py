# -*- coding: utf-8 -*-


class Config(object):
    @classmethod
    def aws_region(cls):
        return 'ap-northeast-1'

    @classmethod
    def aws_role_arn(cls):
        return 'arn:aws:iam::171608821407:role/Cognito_Chikyu_Normal_Id_PoolAuth_Role'

    @classmethod
    def aws_api_gw_service_name(cls):
        return 'execute-api'

    @classmethod
    def host(cls):
        if cls.mode() == 'local':
            return 'localhost:9090'
        elif cls.mode() == 'dev':
            return 'gateway.chikyu.mobi'

    @classmethod
    def protocol(cls):
        if cls.mode() == 'local':
            return 'http'
        elif cls.mode() == 'dev':
            return 'https'

    @classmethod
    def env_name(cls):
        if cls.mode() == 'local':
            return 'local'
        elif cls.mode() == 'dev':
            return 'dev'

    @classmethod
    def mode(cls):
        return 'dev'

