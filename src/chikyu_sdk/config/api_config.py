# -*- coding: utf-8 -*-


class ApiConfig(object):
    __mode = 'prod'

    __HOSTS = {
        'local': 'localhost:9090',
        'docker': 'dev-python:9090',
        'devdc': 'gateway.chikyu.mobi',
        'dev01': 'gateway.chikyu.mobi',
        'dev02': 'gateway.chikyu.mobi',
        'hotfix01': 'gateway.chikyu.mobi',
        'prod': 'endpoint.chikyu.net'
    }

    __PROTOCOLS = {
        'local': 'http',
        'docker': 'http',
        'devdc': 'https',
        'dev01': 'https',
        'dev02': 'https',
        'hotfix01': 'https',
        'prod': 'https'
    }

    __ENV_NAMES = {
        'local': '',
        'docker': '',
        'devdc': 'dev',
        'dev01': 'dev01',
        'dev02': 'dev02',
        'hotfix01': 'hotfix01',
        'prod': ''
    }

    @classmethod
    def aws_region(cls):
        return 'ap-northeast-1'

    @classmethod
    def aws_role_arn(cls):
        if cls.__mode == 'prod':
            return 'arn:aws:iam::171608821407:role/Cognito_chikyu_PROD_idpoolAuth_Role'
        elif cls.__mode == 'docker' or cls.__mode == 'local':
            return 'arn:aws:iam::527083274078:role/Cognito_ChikyuDevLocalAuth_Role'
        else:
            return 'arn:aws:iam::171608821407:role/Cognito_Chikyu_Normal_Id_PoolAuth_Role'

    @classmethod
    def aws_api_gw_service_name(cls):
        return 'execute-api'

    @classmethod
    def host(cls):
        return cls.__HOSTS[cls.mode()]

    @classmethod
    def protocol(cls):
        return cls.__PROTOCOLS[cls.mode()]

    @classmethod
    def env_name(cls):
        return cls.__ENV_NAMES[cls.mode()]

    @classmethod
    def mode(cls):
        if not cls.__mode:
            cls.__mode = 'prod'
        return cls.__mode

    @classmethod
    def set_mode(cls, mode):
        cls.__mode = mode

