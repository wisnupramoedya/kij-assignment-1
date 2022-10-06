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
    def upload_file(uploaded_file: FileStorage, type: int, encryption_type: int, key: str) -> str:
        start: int = time.time_ns()

        path = Path(
            os.path.join(
                current_app.root_path,
                current_app.config[Config.UPLOAD_FOLDER.name],
                secure_filename(uploaded_file.filename)))
        uploaded_file.save(path)

        filename: str = path.name
        filesize: int = os.stat(path).st_size

        end: int = time.time_ns()
        process_time = end - start

        Storage(filename=filename, type=type, encryption_type=encryption_type).save()
        StatisticData(type=type, encryption_type=encryption_type, nanoseconds=process_time, size=filesize).save()

        return url_for('static', filename=Config.STORAGE.value + path.name)