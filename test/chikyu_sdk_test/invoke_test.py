import test_config

from chikyu_sdk.resource.session import Session
from chikyu_sdk.secure_resource import SecureResource
from chikyu_sdk.resource.token import Token

config = test_config.configs


def test_token():
    token = Token.create(config.get('login', 'token_name'), config.get('login', 'email'), config.get('login', 'password'))
    print(token)

    token = Token.renew(token['token_name'], token['login_token'], token['login_secret_token'])

    session = _get_session()
    items = Token.list(session)

    print(items)

    token_name = token['token_name']
    login_token = token['login_token']
    login_secret_token = token['login_secret_token']
    Token.revoke(token_name, login_token, login_secret_token, session)

    session.logout()


def test_secure():
    session = _get_session()

    session.change_organ(1460)
    r = SecureResource(session)

    res = r.invoke('entity/prospects/list',
             {'items_per_page': 10, 'page_index': 0})

    print(res)
    session.logout()


def _get_session():
    return Session.login(config.get('token', 'token_name'),
                         config.get('token', 'login_token'),
                         config.get('token', 'login_secret_token'))
