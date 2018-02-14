import test_config
import os.path
from chikyu_sdk.resource.entity import Entity
from chikyu_sdk.resource.report import Report
from chikyu_sdk.resource.session import Session
from chikyu_sdk.resource.token import Token
from chikyu_sdk.secure_resource import SecureResource

config = test_config.configs


def test_token():
    token_name = 'test_python_token'
    token = Token.create(
        token_name,
        config.get('login', 'email'),
        config.get('login', 'password'),
        86400 * 30 * 12 * 10)

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


def test_report_export():
    session = _get_session()
    session.change_organ(1460)
    r = Report(session)
    res = r.start_export("5731385fb00d26eb22ff7580", Report.FILE_FORMAT_CSV, Report.ENCODING_SJIS, './tmp')
    print(res)


def test_data_import():
    session = _get_session()
    session.change_organ(1460)

    en = Entity(session)
    res = en.start_import('prospects', os.path.join(os.path.dirname(__file__), 'files/test01.csv'),
                    [
                        {'column_name': 'test01', 'field_name': 'last_name'},
                        {'column_name': 'test02', 'field_name': 'first_name'},
                        {'column_name': 'test03', 'field_name': 'company_name'},
                        {'column_name': 'test04', 'field_name': 'prospect_status_div'},
                        {'column_name': 'test05', 'field_name': 'email'}
                    ],
                    {
                        'key_search_option': {
                            'input_method': 'by_name',
                            'input_field_name': ''
                        },
                        'search_related_by_name': True,
                        'field_search_option_list': [

                        ]
                    }, True, 'test2017021301')
    print(res)


def _get_session():
    return Session.login(config.get('token', 'token_name'),
                         config.get('token', 'login_token'),
                         config.get('token', 'login_secret_token'))
