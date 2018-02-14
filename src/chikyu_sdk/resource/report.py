import time
from os import makedirs, path

from chikyu_sdk.helper import http_helper
from chikyu_sdk.resource.resource import Resource


class Report(Resource):
    ENCODING_SJIS = 1
    ENCODING_UTF8 = 2

    FILE_FORMAT_CSV = 1
    FILE_FORMAT_TSV = 2
    FILE_FORMAT_XLSX = 3
    FILE_FORMAT_XLS = 4

    def start_export(self, report_id, file_format, encoding, output_dir, is_async=False):
        res = self._resource.invoke('/report/export/start', {
            "report_flexible_id": report_id,
            "encode_div": encoding,
            "file_format_div": file_format
        })

        export_id = res['export_id']

        if is_async:
            return {'export_id': export_id}

        sts = self.get_export_status(export_id)
        while sts['status'] <= 11:
            sts = self.get_export_status(export_id)
            time.sleep(10)

        is_success = True
        file_path = None
        if sts['status'] == 12 and sts['download_file_path'] and sts['file_name']:
            file_path = path.join(output_dir, sts['file_name'])
            if not path.exists(output_dir):
                makedirs(output_dir)
            http_helper.get_file(sts['download_file_path'], file_path)
        else:
            is_success = False

        return {'export_id': export_id, 'is_success': is_success, 'file_path': file_path}

    def get_export_status(self, export_id):
        return self._resource.invoke('/report/export/status', {'export_id': export_id})
