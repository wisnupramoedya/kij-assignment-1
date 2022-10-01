from distutils.command.upload import upload
from enum import Enum


class Config(Enum):
    UPLOAD_FOLDER = "/api/statics"