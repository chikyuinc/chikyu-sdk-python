# -*- coding: utf-8 -*-
from chikyu_sdk.api_resource import ApiObject
from chikyu_sdk.open_resource import OpenResource
from chikyu_sdk.secure_resource import SecureResource


class Token(ApiObject):
    @classmethod
    def create(cls, token_name, email, password):
        res = OpenResource.invoke('/session/token/create',
                            {'token_name': token_name, 'email': email, 'password': password})
        res['token_name'] = token_name
        return res

    @classmethod
    def renew(cls, token_name, login_token, login_secret_token):
        res = OpenResource.invoke('/session/token/renew', {
            'token_name': token_name,
            'login_token': login_token,
            'login_secret_token': login_secret_token
        })
        res['token_name'] = token_name
        return res

    @classmethod
    def revoke(cls, token_name, login_token, login_secret_token, session):
        SecureResource(session).invoke('/session/token/revoke', {
            'token_name': token_name,
            'login_token': login_token,
            'login_secret_token': login_secret_token
        })

    @classmethod
    def list(cls, session):
        return SecureResource(session).invoke('/session/token/list', {})
