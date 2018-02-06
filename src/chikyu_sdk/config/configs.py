# -*- coding: utf-8 -*-

from os.path import dirname, exists
from ConfigParser import SafeConfigParser

AWS_REGION = 'ap-northeast-1'
AWS_ROLE_ARN = 'arn:aws:iam::171608821407:role/Cognito_Chikyu_Normal_Id_PoolAuth_Role'
AWS_API_GW_SERVICE_NAME = 'execute-api'
ENV_NAME = 'devdc'


__config_path = "{}/config.ini".format(dirname(__file__))
if exists(__config_path):
    conf = SafeConfigParser()
    conf.read(__config_path)
    IS_LOCAL = conf.get('local', 'is_local') == '1'
    AWS_COGNITO_IDENTITY_POOL_ID = conf.get('aws', 'cognito_identity_pool_id')
else:
    IS_LOCAL = False
    AWS_COGNITO_IDENTITY_POOL_ID = None

if IS_LOCAL:
    print("*** LOCAL(dev) MODE ENABLED ***")
    HOST = 'localhost:9090'
    PROTOCOL = 'http'
else:
    HOST = 'cxpybqnsd0.execute-api.ap-northeast-1.amazonaws.com'
    PROTOCOL = 'https'
