import time
import os.path

from chikyu_sdk.error.common_errors import ApiExecuteException
from chikyu_sdk.helper import http_helper
from chikyu_sdk.resource.resource import Resource


class Entity(Resource):
    __END_STATUSES = [23, 22, 42, 34, 99]

    def start_import(self, collection_name, file_path,
                     field_mappings, options, is_create_only, list_name, content_type="text/csv", is_async=False):
        if not os.path.exists(file_path):
            raise ApiExecuteException("file does not exist: {}".format(file_path))

        res = self._resource.invoke('/entity/{}/import/init'.format(collection_name),
                                    {'file_encoding': 'utf8'})

        file_upload_url = res['file_upload_url']

        if not http_helper.put_file(file_upload_url, file_path, content_type):
            return {'import_id': None}

        res = self._resource.invoke('/entity/{}/import/start'.format(collection_name),
                                    {'file_upload_url': file_upload_url,
                                     'field_mappings': field_mappings,
                                     'options': options,
                                     'is_create_only': is_create_only,
                                     'list_name': list_name})

        import_id = res['import_id']

        if is_async:
            return {'import_id': import_id}

        sts = self._resource.invoke(
            '/entity/{}/import/status'.format(collection_name), {'import_id': import_id})

        while sts['status'] not in self.__END_STATUSES:
            sts = self._resource.invoke(
                '/entity/{}/import/status'.format(collection_name), {'import_id': import_id})
            time.sleep(10)

        sts['import_id'] = import_id
        sts['is_success'] = sts['status'] == 42
        return sts
