import codecs
from encryptions.contracts.encryption import Encryption


class RC4(Encryption):
    length: int = 32

    def KSA(self, key: str):
        key_length = len(key)

        S = list(range(self.length))
        j = 0
        for i in range(self.length):
            j = (j + S[i] + key[i % key_length]) % self.length
            S[i], S[j] = S[j], S[i]  # swap values

        return S

    def PRGA(self, S: list[int]):
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
        key = [ord(c) for c in key]
        text = [ord(c) for c in text]

        keystream = self.get_keystream(key)

        res = []
        for c in text:
            val = ("%02X" % (c ^ next(keystream)))  # XOR and taking hex
            res.append(val)
        return ''.join(res)

    def decrypt(self, key: str, text: bytes) -> bytes:
        text = codecs.decode(text, 'hex_codec')

        key = [ord(c) for c in key]

        keystream = self.get_keystream(key)

        res = []
        for c in text:
            val = ("%02X" % (c ^ next(keystream)))  # XOR and taking hex
            res.append(val)
        return codecs.decode(''.join(res), 'hex_codec').decode('utf-8')
