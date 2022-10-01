from flask import Blueprint, request
from werkzeug.utils import secure_filename
from ..common.url import Url

encryption_controller = Blueprint('encryption_controller', __name__)


@encryption_controller.route(Url.ENCRYPT_URL.value, methods=[Url.GET.value, Url.POST.value])
def encrypt():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'file uploaded successfully'
