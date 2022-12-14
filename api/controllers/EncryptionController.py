from flask import Blueprint, request, redirect, current_app, jsonify, url_for, Response
from flask_cors import cross_origin
from werkzeug.datastructures import CombinedMultiDict
from api.common.url import Url
from api.request.upload_encryption import UploadEncryptionRequest
from api.services.UploadFileService import UploadFileService
from api.common.encryption import Type, EncryptionType

encryption_controller = Blueprint('encryption_controller', __name__)


@encryption_controller.route(Url.ENCRYPT_URL.value, methods=[Url.POST.value])
@cross_origin()
def encrypt():
    """
    Url: /encrypt
    This used to upload file to be encrypted by server.
    Still need to add thread service for encryption
    """
    if request.method == 'POST':
        form: UploadEncryptionRequest = UploadEncryptionRequest(CombinedMultiDict((request.form, request.files)))
        if not form.validate_on_submit():
            return jsonify(status_code=403, message=form.errors), 403

        encryption_type = form.encryption_type.data
        key = form.key.data
        uploaded_file = form.uploaded_file.data

        if uploaded_file.filename == '':
            return jsonify(status_code=400, message='file not found'), 400

        encrypted_file_path = UploadFileService.upload_file(uploaded_file, Type.ENCRYPT.value, encryption_type, key)

        return jsonify(status_code=200, data={'encrypted_file': encrypted_file_path}, message='file uploaded successfully'), 200

@encryption_controller.route(Url.DECRYPT_URL.value, methods=[Url.POST.value])
@cross_origin()
def decrypt():
    """
    Url: /decrypt
    This used to upload file to be decrypted by server.
    Still need to add thread service for decryption
    """
    if request.method == 'POST':
        form: UploadEncryptionRequest = UploadEncryptionRequest(CombinedMultiDict((request.form, request.files)))
        if not form.validate_on_submit():
            return jsonify(status_code=403, message=form.errors), 403

        encryption_type = form.encryption_type.data
        key = form.key.data
        uploaded_file = form.uploaded_file.data

        if uploaded_file.filename == '':
            return jsonify(status_code=400, message='file not found'), 400

        decrypted_file_path = UploadFileService.upload_file(uploaded_file, Type.DECRYPT.value, encryption_type, key)

        return jsonify(status_code=200, data={'encrypted_file': decrypted_file_path}, message='file uploaded successfully'), 200

@encryption_controller.route(Url.ALL_UPLOADED_URL.value, methods=[Url.GET.value])
@cross_origin()
def get_all():
    if request.method == 'GET':
        storages = UploadFileService.get_all_uploaded_file()

        if len(storages) == 0:
            return Response(
                '{"status_code": 404, "data": {"storages": ' + storages.to_json() + '}, "mesagge": "storage\'s data is not found"}',
                mimetype='application/json',
                status=404
            )

        return Response(
            '{"status_code": 200, "data": {"storages": ' + storages.to_json() + '}, "mesagge": "get all storage\'s data successfully"}',
            mimetype='application/json',
            status=200
        )

