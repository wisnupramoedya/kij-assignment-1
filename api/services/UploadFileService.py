import threading

from flask import url_for, current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import os
from pathlib import Path
from api.common.config import Config
from api.repositories.database import Storage, StatisticData
import time

class UploadFileService:
    @staticmethod
    def upload_file(uploaded_file: FileStorage, tipe: int, encryption_type: int, key: str) -> str:
        start: int = time.time_ns()

        path = Path(
            os.path.join(
                current_app.root_path,
                current_app.config[Config.UPLOAD_FOLDER.name],
                secure_filename(uploaded_file.filename)))
        uploaded_file.save(path)
        print(path)

        filename: str = path.name
        filesize: int = os.stat(path).st_size

        end: int = time.time_ns()
        process_time = end - start

        # bikin thread service buat mindahin file ke folder encrypt atau decrypt tergantung type-nya
        thread = threading.Thread(target=UploadFileService.move_uploaded_file, args=(uploaded_file, tipe, key, path,))
        thread.start()

        Storage(filename=filename, type=tipe, encryption_type=encryption_type).save()
        StatisticData(type=tipe, encryption_type=encryption_type, nanoseconds=process_time, size=filesize).save()

        return url_for('static', filename=Config.STORAGE.value + path.name)

    @staticmethod
    def get_all_uploaded_file():
        storages = Storage.objects()
        return storages

    @staticmethod
    def move_uploaded_file(uploaded_file: FileStorage, tipe: int, key: str, old_path: Path):
        if tipe == 1:
            path = os.path.split(old_path)
            new_path = Path(
                os.path.join(
                    path[0],
                    'Encrypt',
                    path[1]))
            os.replace(old_path, new_path)
        else:
            path = os.path.split(old_path)
            new_path = Path(
                os.path.join(
                    path[0],
                    'Decrypt',
                    path[1]))
            os.replace(old_path, new_path)