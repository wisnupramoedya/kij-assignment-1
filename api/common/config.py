from distutils.command.upload import upload
from enum import Enum
import os


class Config(Enum):
    STORAGE = "storages/"
    UPLOAD_FOLDER = "api/statics/" + STORAGE