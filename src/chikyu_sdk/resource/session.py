# -*- coding: utf-8 -*-

from chikyu_sdk.api_resource import ApiObject
from boto3 import client as boto3_client

from chikyu_sdk.config import configs
from chikyu_sdk.open_resource import OpenResource
from chikyu_sdk.secure_resource import SecureResource


class Credentials(object):
    def __init__(self, key_id, secret_key, session_token):
        super(Credentials, self).__init__()
        self.__key_id = key_id
        self.__secret_key = secret_key
        self.__session_token = session_token

    @property
    def key_id(self):
        pass

    @property
    def secret_key(self):
        pass

    @property
    def session_token(self):
        pass

    @key_id.getter
    def key_id(self):
        return self.__key_id

    @secret_key.getter
    def secret_key(self):
        return self.__secret_key

    @session_token.getter
    def session_token(self):
        return self.__session_token


class Session(ApiObject):
    def __init__(self, credentials, session_id, api_key, identity_id):
        super(Session, self).__init__()
        self.__credentials = credentials
        self.__session_id = session_id
        self.__api_key = api_key
        self.__identity_id = identity_id

    @classmethod
    def login(cls, token_name, login_token, login_secret_token):
        login_result = OpenResource.invoke('/session/login', {
            'token_name': token_name,
            'login_token': login_token,
            'login_secret_token': login_secret_token
        })

        res = boto3_client("sts").assume_role_with_web_identity(
            RoleArn=configs.AWS_ROLE_ARN,
            RoleSessionName=configs.AWS_API_GW_SERVICE_NAME,
            WebIdentityToken=login_result['cognito_token']
        )

        return Session(
            credentials=Credentials(res['Credentials']['AccessKeyId'],
                                    res['Credentials']['SecretAccessKey'],
                                    res['Credentials']['SessionToken']),
            session_id=login_result['session_id'],
            api_key=login_result['api_key'],
            identity_id=login_result['cognito_identity_id']
        )

    def change_organ(self, organ_id):
        res = SecureResource(self).invoke('/session/organ/change', {'target_organ_id': organ_id})
        self.__api_key = res['api_key']

    def logout(self):
        SecureResource(self).invoke('/session/logout', {})
        self.__api_key = None
        self.__session_id = None
        self.__credentials = None

    @property
    def credentials(self):
        pass

    @property
    def session_id(self):
        pass

    @property
    def api_key(self):
        pass

    @property
    def identity_id(self):
        pass

    @credentials.getter
    def credentials(self):
        return self.__credentials

    @session_id.getter
    def session_id(self):
        return self.__session_id

    @api_key.getter
    def api_key(self):
        return self.__api_key

    @identity_id.getter
    def identity_id(self):
        return self.__identity_id
