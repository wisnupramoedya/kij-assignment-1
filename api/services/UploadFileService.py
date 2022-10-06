from flask import url_for, current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import os
from pathlib import Path
from api.common.config import Config

class UploadFileService:
    @staticmethod
    def upload_file(uploaded_file: FileStorage) -> str:
        path = Path(
            os.path.join(
                current_app.root_path,
                current_app.config[Config.UPLOAD_FOLDER.name],
                secure_filename(uploaded_file.filename)))

        uploaded_file.save(path)

        return url_for('static', filename=Config.STORAGE.value + path.name)