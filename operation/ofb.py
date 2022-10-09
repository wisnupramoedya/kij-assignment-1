import math
from encryptions.contracts.encryption import Encryption
import codecs


class OFB:
    IV: bytes
    encryption_class: Encryption

    def __init__(self, IV: bytes) -> None:
        self.IV = IV

    def set_class(self, encryption_class: Encryption):
        self.encryption_class = encryption_class
        return self

    def encrypt(self, key: str, plain_text: bytes) -> bytes:
        block_size = self.encryption_class.length
        blocks = math.ceil(len(plain_text) / block_size)
        block_text = [plain_text[i * block_size: (i + 1) * block_size]
                      for i in range(int(len(plain_text) / block_size))]
        # print(len(block_text))

        if len(plain_text) % block_size != 0:
            block_text.append(self.padding(plain_text, block_size))

        cipher_text: bytes = b''
        encrypted: bytes = self.encryption_class.encrypt(key, self.IV)

        # print(block_text)
        # print(block_text[0])
        # print(type(block_text[0]))
        # print(encrypted)
        # print(encrypted.hex())
        # utf = encrypted.decode('utf-8',errors='replace')
        # print(utf)
        # print(type(encrypted))
        block_cipher_text = bytearray(b'')
        for i in range(len(block_text)):
            # print(f'block_text {i} = {len(block_text[i])}')
            # print(f'encrypted = {len(encrypted)}')
            # new_cipher_text = [bytes(a ^ b)
            #                    for a, b in zip(block_text[i], encrypted)]
            n_block_text = codecs.encode(block_text[i], 'hex')
            n_block_text = self.hextobin(n_block_text)
            bin_encrypted = codecs.encode(encrypted, 'hex')
            bin_encrypted = self.hextobin(bin_encrypted)
            new_cipher_text = self.xor(n_block_text, bin_encrypted)
            new_cipher_text = bytes.fromhex(self.bintohex(new_cipher_text))

            block_cipher_text.extend(new_cipher_text)

            # error: UnicodeDecodeError: 'utf-8' codec can't decode byte 0xee in position 0: invalid continuation byte
            # encrypted = self.encryption_class.encrypt(encrypted.decode('utf-8',errors='replace'), self.IV)
            encrypted = self.encryption_class.encrypt(key, encrypted)

            cipher_text = bytes(block_cipher_text)

        print('done')

        return cipher_text

    def decrypt(self, key: str, cipher_text: bytes) -> bytes:
        block_size = self.encryption_class.length

        block_text = [cipher_text[i * block_size: (i + 1) * block_size]
                      for i in range(int(len(cipher_text) / block_size))]
        # print(int(len(cipher_text) / block_size))

        decrypted: bytes = self.encryption_class.encrypt(key, self.IV)

        block_plain_text = bytearray(b'')
        for i in range(len(block_text)):
            # new_plain_text = [bytes(ord(a) ^ ord(b))
            #                   for a, b in zip(block_text[i], decrypted)]
            n_block_text = codecs.encode(block_text[i], 'hex')
            n_block_text = self.hextobin(n_block_text)
            bin_decrypted = codecs.encode(decrypted, 'hex')
            bin_decrypted = self.hextobin(bin_decrypted)
            new_plain_text = self.xor(n_block_text, bin_decrypted)
            new_plain_text = bytes.fromhex(self.bintohex(new_plain_text))
            if i == len(block_text)-1:
                new_plain_text = self.unpadding(new_plain_text)

            block_plain_text.extend(new_plain_text)
            # plain_text += b''.join(new_plain_text)
            decrypted = self.encryption_class.encrypt(key, decrypted)

        plain_text = bytes(block_plain_text)
        print('done')
        return plain_text

    def xor_strings(self, a, b):
        res = int(a, 16) ^ int(b, 16)
        return '{:x}'.format(res)

    def hextobin(self, hexval):
        thelen = len(hexval) * 4
        binval = bin(int(hexval, 16))[2:]
        while (len(binval)) < thelen:
            binval = '0' + binval
        return binval

    def bintohex(self, binval):
        mp = {"0000": '0',
              "0001": '1',
              "0010": '2',
              "0011": '3',
              "0100": '4',
              "0101": '5',
              "0110": '6',
              "0111": '7',
              "1000": '8',
              "1001": '9',
              "1010": 'A',
              "1011": 'B',
              "1100": 'C',
              "1101": 'D',
              "1110": 'E',
              "1111": 'F'}
        res = ''
        for i in range(0, len(binval), 4):
            ch = ""
            ch = ch + binval[i]
            ch = ch + binval[i + 1]
            ch = ch + binval[i + 2]
            ch = ch + binval[i + 3]
            res = res + mp[ch]

        return res

    def xor(self, arr, key):
        ans = ''
        for i in range(len(arr)):
            if arr[i] == key[i]:
                ans = ans + '0'
            else:
                ans = ans + '1'
        return ans

    def padding(self, plain_text, block_size):
        val = ['01', '02', '03', '04', '05', '06', '07', '08',
               '09', '0A', '0B', '0C', '0D', '0E', '0F', '10']
        block_len = int(len(plain_text) / block_size)
        start = int(block_len * block_size)
        end = len(plain_text)
        padded_hex = ''
        for i in range(start, end):
            padded_hex = padded_hex + "{0:02x}".format(plain_text[i])

        padded_hex = padded_hex + (val[start+block_size-end-1]*(start+block_size-end))
        # print(f'padded: {padded_hex}')
        return bytes.fromhex(padded_hex)

    def unpadding(self, plain_text):
        val = ['01', '02', '03', '04', '05', '06', '07', '08',
               '09', '0a', '0b', '0c', '0d', '0e', '0f', '10']

        for i in range(len(val)):
            temp = codecs.encode(plain_text[(0 - (i + 1)):], 'hex')
            if temp == (val[i] * (i+1)).encode():
                return plain_text[:(0-(i+1))]

        return plain_text
