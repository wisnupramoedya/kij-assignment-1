import codecs
from encryptions.contracts.encryption import Encryption

class RC4(Encryption):
    length: int = 256

    def KSA(self, key: str):
        key_length = len(key)
        S, T = [], []
        for i in range(0, 256):
            S.append(i)
            T.append(ord(key[i % len(key)]))

        j = 0
        for i in range(self.length):
            j = (j + S[i] + T[i]) % self.length
            S[i], S[j] = S[j], S[i]  # swap values

        return S

    def PRGA(self, S):
        i = 0
        j = 0
        while True:
            i = (i + 1) % self.length
            j = (j + S[i]) % self.length

            S[i], S[j] = S[j], S[i]  # swap values
            K = S[(S[i] + S[j]) % self.length]
            yield K

    def get_keystream(self, key: str):
        S = self.KSA(key)
        return self.PRGA(S)

    def encrypt(self, key: str, text: bytes) -> bytes:
        key_array = []
        text_array = []

        key = [format(c) for c in key]
        text = [format(c) for c in text]

        for texts in text:
            text_array.insert(0, texts.encode()[0])

        for keys in key:
            key_array.insert(0, keys.encode()[0])

        keystream = self.get_keystream(key)

        res = []
        for c in text:
            # print(type(c))
            # print(type(next(keystream)))
            val = ("%02X" % (int(c) ^ next(keystream)))  # XOR and taking hex
            res.append(val)
        print (''.join(res))
        bytes_object = bytes.fromhex(''.join(res))
        return bytes_object

    def decrypt(self, key: str, text: bytes) -> bytes:
        # text = codecs.decode(text, 'hex_codec')
        key_array = []
        key = [format(c) for c in key]

        for keys in key:
            key_array.insert(0, keys.encode()[0])

        keystream = self.get_keystream(key)

        res = []
        for c in text:
            val = ("%02X" % (c ^ next(keystream)))  # XOR and taking hex
            res.append(val)
        print('done')
        return codecs.decode(''.join(res), 'hex_codec')
