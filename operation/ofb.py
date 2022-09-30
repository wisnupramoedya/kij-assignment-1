from typing import Callable


class OFB:
    IV: str
    BLOCKSIZE: int = 128

    def __init__(self, IV: str) -> None:
        self.IV = IV

    def encrypt(self, key: str, plain_text: str, encryption: Callable[[str, str], str]):
        block_text = [plain_text[i*self.BLOCKSIZE: (i+1)*self.BLOCKSIZE]
                      for i in range(int(len(plain_text)/self.BLOCKSIZE))]

        cipher_text: str = ''
        encrypted: str = encryption(key, self.IV)
        print(encrypted)

        for i in range(len(block_text)):
            new_cipher_text = [chr(ord(a) ^ ord(b))
                               for a, b in zip(block_text[i], encrypted)]
            cipher_text += "".join(new_cipher_text)
            encrypted = encryption(encrypted, self.IV)
            print(encrypted)
            print('Cipher' + cipher_text)

        return cipher_text

    def decrypt(self, key: str, cipher_text: str, decryption: Callable[[str, str], str]):
        block_text = [cipher_text[i*self.BLOCKSIZE: (i+1)*self.BLOCKSIZE]
                      for i in range(int(len(plain_text)/self.BLOCKSIZE))]

        plain_text: str = ''
        decrypted: str = decryption(key, self.IV)

        for i in range(len(block_text)):
            new_plain_text = [chr(ord(a) ^ ord(b))
                              for a, b in zip(block_text[i], decrypted)]
            plain_text += "".join(new_plain_text)
            decrypted = decryption(decrypted, self.IV)

        return plain_text


def encryption(key: str, text: str) -> str:
    cipher_text: str = ''
    for i in range(len(text)):
        cipher_text += chr(ord(text[i]) + ord(key[i % len(key)]) - 96)

    return cipher_text


key = "aaa"
text = "halosayawisnu"

print(encryption("aaa", "halosayawisnu"))
ofb = OFB("aaaaaa")
print(ofb.encrypt(key, text, encryption))
