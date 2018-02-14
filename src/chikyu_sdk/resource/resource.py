from chikyu_sdk.secure_resource import SecureResource
from logging import getLogger


class Resource(object):
    _logger = getLogger(__name__)

    def __init__(self, session):
        self._session = session
        self._resource = SecureResource(self._session)
