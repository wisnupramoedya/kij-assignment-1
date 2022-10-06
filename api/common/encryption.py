from enum import Enum

class Type(Enum):
    ENCRYPT = 1
    DECRYPT = 2

class EncryptionType(Enum):
    AES = 1
    DES = 2
    RC4 = 3