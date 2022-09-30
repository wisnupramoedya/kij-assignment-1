import codecs
from encryptions.contracts.encryption import Encryption


class RC4(Encryption):
    def encrypt(key: str, plain_text: bytes) -> bytes:
        """Kode untuk melakukan encrypt"""
        pass

    def decrypt(key: str, cipher_text: bytes) -> bytes:
        """Kode untuk melakukan decrypt"""
        pass


def KSA(key):
    key_length = len(key)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]  # swap values

    return S


def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256

        S[i], S[j] = S[j], S[i]  # swap values
        K = S[(S[i] + S[j]) % 256]
        yield K


def get_keystream(key):
    S = KSA(key)
    return PRGA(S)


def encrypt(key, text):

    key = [ord(c) for c in key]
    text = [ord(c) for c in text]

    keystream = get_keystream(key)

    res = []
    for c in text:
        val = ("%02X" % (c ^ next(keystream)))  # XOR and taking hex
        res.append(val)
    return ''.join(res)


def decrypt(key, text):
    text = codecs.decode(text, 'hex_codec')

    key = [ord(c) for c in key]

    keystream = get_keystream(key)

    res = []
    for c in text:
        val = ("%02X" % (c ^ next(keystream)))  # XOR and taking hex
        res.append(val)
    return codecs.decode(''.join(res), 'hex_codec').decode('utf-8')
