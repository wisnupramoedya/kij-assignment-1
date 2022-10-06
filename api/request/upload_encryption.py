from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import IntegerField, StringField, validators
from wtforms.validators import DataRequired, NumberRange

class UploadEncryptionRequest(FlaskForm):
    class Meta:
        csrf = False

    encryption_type = IntegerField('encryption_type', validators=[
        DataRequired(),
        NumberRange(min=1, max=3)
    ])
    key = StringField('key', validators=[
        DataRequired()
    ])
    uploaded_file = FileField('uploaded_file', validators=[
        FileRequired()
    ])