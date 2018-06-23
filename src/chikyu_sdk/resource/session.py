# -*- coding: utf-8 -*-
import json

from chikyu_sdk.api_resource import ApiObject
from boto3 import client as boto3_client

from chikyu_sdk.config.api_config import ApiConfig
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

    def to_dict(self):
        return {
            'access_key_id': self.key_id,
            'secret_access_key': self.secret_key,
            'session_token': self.session_token
        }

    @classmethod
    def from_dict(cls, item):
        return Credentials(item['access_key_id'], item['secret_access_key'], item['session_token'])

    def __str__(self):
        return json.dumps(self.to_dict())


class Session(ApiObject):
    def __init__(self, credentials, session_id, api_key, identity_id, user):
        super(Session, self).__init__()
        self.__credentials = credentials
        self.__session_id = session_id
        self.__api_key = api_key
        self.__identity_id = identity_id
        self.__user = user

    @classmethod
    def login(cls, token_name, login_token, login_secret_token, duration=86400):
        login_result = OpenResource.invoke('/session/login', {
            'token_name': token_name,
            'login_token': login_token,
            'login_secret_token': login_secret_token,
            'duration': duration
        })

        res = boto3_client("sts").assume_role_with_web_identity(
            RoleArn=ApiConfig.aws_role_arn(),
            RoleSessionName=ApiConfig.aws_api_gw_service_name(),
            WebIdentityToken=login_result['cognito_token'],
            DurationSeconds=43200
        )

        return Session(
            credentials=Credentials(res['Credentials']['AccessKeyId'],
                                    res['Credentials']['SecretAccessKey'],
                                    res['Credentials']['SessionToken']),
            session_id=login_result['session_id'],
            api_key=login_result['api_key'],
            identity_id=login_result['cognito_identity_id'],
            user=login_result['user']
        )

    def change_organ(self, organ_id):
        res = SecureResource(self).invoke('/session/organ/change', {'target_organ_id': organ_id})
        self.__api_key = res['api_key']
        self.__user = res['user']

    def logout(self):
        SecureResource(self).invoke('/session/logout', {})
        self.__api_key = None
        self.__session_id = None
        self.__credentials = None
        self.__user = None

    def to_dict(self):
        return {
            'api_key': self.__api_key,
            'session_id': self.__session_id,
            'credentials': self.__credentials.to_dict(),
            'identity_id': self.__identity_id,
            'user': self.__user
        }

    @classmethod
    def from_json(cls, json_str):
        item = json.loads(json_str)
        return cls.from_dict(item)

    @classmethod
    def from_dict(cls, item):
        return Session(Credentials.from_dict(
            item['credentials']), item['session_id'], item['api_key'], item['identity_id'], item['user']
        )

    def __str__(self):
        return json.dumps(self.to_dict())

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
