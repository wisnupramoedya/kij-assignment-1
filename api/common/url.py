from enum import Enum

class Url(Enum):
    GET = "GET"
    POST = "POST"

    ENCRYPT_URL = "/encrypt"
    ENCRYPTED_URL = "/encrypted"
    DECRYPT_URL = "/decrypt"
    DECRYPTED_URL = "/decrypted"

    ALL_UPLOADED_URL = "/all"