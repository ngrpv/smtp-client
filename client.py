import base64
import os.path
from mimetypes import types_map

BOUNDARY = '----==--bound.53245.vla1-5245e79bed88.qloud-c.yandex.net'


class Smtp:
    def __init__(self, user_mail: str):
        self._mail = user_mail
        self._attachments = []

    def attach(self, filename: str):
        if not os.path.exists(filename):
            raise FileExistsError(f'{filename} not exists')
        self._attachments.append(filename)

    def get_smtp_data(self, title: str, message_text: str,
                      destination_address: str) -> str:

        message = (f'From: {self._mail}\n'
                   f'To: {destination_address}\n'
                   f'Subject: {title} \n'
                   'MIME-Version: 1.0 \n'
                   f'Content-Type: multipart/mixed;\n'
                   f'\tboundary="{BOUNDARY}"\n\n'
                   f'--{BOUNDARY}\n'
                   'Content-Type: text/plain; charset=utf-8\n'
                   'Content-Transfer-Encoding: 8bit\n\n'

                   f'{message_text}\n')
        for attachment in self._attachments:
            message += self._get_attachment_data(attachment)
        message += f'--{BOUNDARY}--\n.\n'
        return message

    @staticmethod
    def _get_attachment_data(filename: str) -> str:
        type = ''
        try:
            type = types_map["." + filename.split(".")[-1]]
        except KeyError:
            raise KeyError(f'Undefined mime type for {filename}')
        data = (f'--{BOUNDARY}\n'
                f'Content-Disposition: attachment;\n'
                f'\tfilename="{filename.split("/")[-1]}"\n'
                'Content-Transfer-Encoding: base64\n'
                f'Content-Type: {type};\n'
                f'\tname="{filename.split("/")[-1]}"\n\n')
        with open(filename, 'rb') as f:
            b64_encoded = base64.b64encode(f.read())
            data += b64_encoded.decode() + '\n'
        return data
