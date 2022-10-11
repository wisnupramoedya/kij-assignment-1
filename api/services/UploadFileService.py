import threading

from flask import url_for, current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import os
from pathlib import Path
from api.common.config import Config
from api.repositories.database import Storage, StatisticData
from api.common.encryption import Type, EncryptionType
import time

from encryptions.contracts.encryption import Encryption
from encryptions.aes import AES
from encryptions.des import DES
from encryptions.rc4 import RC4
from operation.ofb import OFB


class UploadFileService:
    @staticmethod
    def upload_file(uploaded_file: FileStorage, method_type: int, encryption_type: int, key: str) -> str:

        path = Path(
            os.path.join(
                current_app.root_path,
                current_app.config[Config.UPLOAD_FOLDER.name],
                str.lower(Type(method_type).name),
                secure_filename(time.strftime("%Y%m%d-%H%M%S_") + uploaded_file.filename)))

        real_name = uploaded_file.filename;
        uploaded_file.save(path)


        filename: str = path.name

        # bikin thread service buat mindahin file ke folder encrypt atau decrypt tergantung type-nya
        thread = threading.Thread(target=UploadFileService.move_uploaded_file, args=(method_type, encryption_type, key, path, filename,))
        thread.start()

        Storage(filename=filename, real_name=real_name, type=method_type, encryption_type=encryption_type).save()

        return url_for('static', filename=Config.STORAGE.value + path.name)

    @staticmethod
    def get_all_uploaded_file():
        storages = Storage.objects()
        return storages

    @staticmethod
    def move_uploaded_file(method_type: int, encryption_type: int, key: str, old_path: Path, filename: str):
        filesize: int = os.stat(old_path).st_size
        start: int = time.time_ns()

        encryption = object()
        if encryption_type == EncryptionType.AES.value:
            encryption = AES()
        elif encryption_type == EncryptionType.DES.value:
            encryption = DES()
        elif encryption_type == EncryptionType.RC4.value:
            encryption = RC4()

        if method_type == Type.ENCRYPT.value:
            f = open(old_path, 'rb')
            content = f.read()
            cipher_text = OFB(b'isfhryusvby2346_346asddssttkksogicb)adhjuxchbuhwetgsgh__110625sd35gjhv').set_class(
                encryption).encrypt(key, content)
            f.close()
            # print(content)
            wr = open(old_path, 'wb')
            wr.write(cipher_text)
            wr.close()
        else:
            f = open(old_path, 'rb')
            content = f.read()
            cipher_text = OFB(b'isfhryusvby2346_346asddssttkksogicb)adhjuxchbuhwetgsgh__110625sd35gjhv').set_class(
                encryption).decrypt(key, content)
            f.close()
            # print(content)
            wr = open(old_path, 'wb')
            wr.write(cipher_text)
            wr.close()

        end: int = time.time_ns()
        process_time = end - start
        StatisticData(type=method_type, encryption_type=encryption_type, nanoseconds=process_time, size=filesize).save()
        Storage.objects(filename=filename).update(done_encrypted=True)
