from mongoengine import Document, StringField, DateTimeField, EnumField, LongField, BooleanField
from datetime import datetime
from api.common.encryption import Type, EncryptionType

class Storage(Document):
    filename = StringField()
    real_name = StringField()
    type = EnumField(Type, default=Type.ENCRYPT)
    encryption_type = EnumField(EncryptionType, default=EncryptionType.AES)
    done_encrypted = BooleanField(default=False)
    created_date = DateTimeField(default=datetime.utcnow)

class StatisticData(Document):
    filename = StringField()
    type = EnumField(Type, default=Type.ENCRYPT)
    encryption_type = EnumField(EncryptionType, default=EncryptionType.AES)
    nanoseconds = LongField()
    size = LongField()