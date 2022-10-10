from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired, NumberRange, Length, ValidationError

def FileSizeLimit(max_size_in_mb):
    max_bytes = max_size_in_mb*1024*1024
    def file_length_check(form, field):
        if len(field.data.read()) > max_bytes:
            raise ValidationError(f"File size must be less than {max_size_in_mb}MB")
        field.data.seek(0)
    return file_length_check


class UploadEncryptionRequest(FlaskForm):
    class Meta:
        csrf = False

    encryption_type = IntegerField('encryption_type', validators=[
        DataRequired(),
        NumberRange(min=1, max=3)
    ])
    key = StringField('key', validators=[
        DataRequired(),
        Length(min=8, max=128)
    ])
    uploaded_file = FileField('uploaded_file', validators=[
        FileRequired(),
        FileSizeLimit(max_size_in_mb=60)
    ])