from encryptions.contracts.encryption import Encryption

class OFB:
    IV: str
    encryption_class: Encryption

    def __init__(self, IV: str) -> None:
        self.IV = IV

    def set_class(self, encryption_class: Encryption):
        self.encryption_class = encryption_class
        return self

    def encrypt(self, key: str, plain_text: bytes) -> bytes:
        block_size = self.encryption_class.length
        block_text = [plain_text[i*block_size: (i+1)*block_size]
                      for i in range(int(len(plain_text)/block_size))]

        cipher_text: bytes = b''
        encrypted: bytes = self.encryption_class.encrypt(key, self.IV)

        # print(block_text)
        # print(block_text[0])
        # print(type(block_text[0]))
        # print(encrypted)
        # print(type(encrypted))
        for i in range(len(block_text)):
            new_cipher_text = [bytes(a ^ b)
                               for a, b in zip(block_text[i], encrypted)]
            cipher_text += b''.join(new_cipher_text)

            # error: UnicodeDecodeError: 'utf-8' codec can't decode byte 0xee in position 0: invalid continuation byte
            encrypted = self.encryption_class.encrypt(str(encrypted, "utf-8"), self.IV)

        return cipher_text

    def decrypt(self, key: str, cipher_text: bytes) -> bytes:
        block_size = self.encryption_class.length
        block_text = [cipher_text[i*block_size: (i+1)*block_size]
                      for i in range(int(len(plain_text)/block_size))]

        plain_text: bytes = b''
        decrypted: bytes = self.encryption_class.decrypt(key, self.IV)

        for i in range(len(block_text)):
            new_plain_text = [bytes(ord(a) ^ ord(b))
                              for a, b in zip(block_text[i], decrypted)]
            plain_text += b''.join(new_plain_text)
            decrypted = self.encryption_class.decrypt(decrypted, self.IV)

        return plain_text

