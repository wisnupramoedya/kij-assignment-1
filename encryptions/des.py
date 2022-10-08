import codecs
from encryptions.contracts.encryption import Encryption


class DES(Encryption):
    length: int = 8

    def __init__(self):
        self.permutasi_awal = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
                               62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
                               57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
                               61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7]

        self.ekspansi = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9,
                         8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17,
                         16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25,
                         24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]

        self.key_permutation = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
                                10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
                                63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
                                14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]

        self.shift_bit = [1, 1, 2, 2,
                          2, 2, 2, 2,
                          1, 2, 2, 2,
                          2, 2, 2, 1]

        self.permutasi_kompresi = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10,
                                   23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2,
                                   41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
                                   44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]

        # Ada 8 S-box
        self.s_box = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
                       [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
                       [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
                       [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

                      [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
                       [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
                       [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
                       [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

                      [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
                       [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
                       [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
                       [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

                      [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
                       [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
                       [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
                       [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

                      [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
                       [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
                       [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
                       [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

                      [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
                       [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
                       [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
                       [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

                      [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
                       [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
                       [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
                       [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

                      [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
                       [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
                       [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
                       [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]

        self.p_box = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 8, 31, 10,
                      2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25]

        self.inverse_permutasi_awal = [40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
                                       38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
                                       36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
                                       34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25]

    def encrypt(self, key: str, plain_text: bytes) -> bytes:
        # print(plain_text)
        new_key = self.process_key(key)
        cipher_text = self.encrypt_process(new_key, plain_text)

        return cipher_text


    def decrypt(self, key: str, cipher_text: bytes) -> bytes:
        new_key = self.process_key(key)
        decrypt_key = new_key[::-1]
        text = self.encrypt_process(decrypt_key, cipher_text)

        return text

    def encrypt_process(self, key: str, plain_text: bytes) -> bytes:
        plain_text = codecs.encode(plain_text, 'hex')
        plain_text = self.hextobin(plain_text)
        p_text = self.permutasi(plain_text, self.permutasi_awal, len(self.permutasi_awal))

        l = p_text[0:int(len(p_text) / 2)]
        r = p_text[int(len(p_text) / 2):len(p_text)]
        for i in range(0, 16):
            ekspansi_r = self.permutasi(r, self.ekspansi, len(self.ekspansi))
            vec_a = self.xor(ekspansi_r, key[i])
            sbox_res = ''
            for j in range(0, 8):
                # bit 1 dan terakhir adalah row, sisanya adalah kolom
                row = self.bin2dec(int(vec_a[j * 6] + vec_a[j * 6 + 5]))
                column = self.bin2dec(int(vec_a[j * 6 + 1] + vec_a[j * 6 + 2] + vec_a[j * 6 + 3] + vec_a[j * 6 + 4]))
                sbox_res = sbox_res + self.dec2bin(self.s_box[j][row][column])

            sbox_res = self.permutasi(sbox_res, self.p_box, len(self.p_box))
            l = self.xor(l, sbox_res)

            if i != 15:
                l, r = r, l

        enchipering = l + r
        cipher_text = self.permutasi(enchipering, self.inverse_permutasi_awal, len(self.inverse_permutasi_awal))
        # convert jadi bytes
        cipher_text = bytes.fromhex(self.bintohex(cipher_text))

        return cipher_text

    def shift_left(self, key, shift_number):
        tmp = ''
        for i in range(shift_number):
            for j in range(1, len(key)):
                tmp = tmp + key[j]
            tmp = tmp + key[0]
            key = tmp
            tmp = ''
        return key

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

    # Binary to decimal conversion

    def bin2dec(self, binary):
        binary1 = binary
        decimal, i, n = 0, 0, 0
        while (binary != 0):
            dec = binary % 10
            decimal = decimal + dec * pow(2, i)
            binary = binary // 10
            i += 1
        return decimal

    # Decimal to binary conversion

    def dec2bin(self, num):
        res = bin(num).replace("0b", "")
        if (len(res) % 4 != 0):
            div = len(res) / 4
            div = int(div)
            counter = (4 * (div + 1)) - len(res)
            for i in range(0, counter):
                res = '0' + res
        return res

    # fungsi menyusun bit-bit sesuai urutan pada tabel
    def permutasi(self, text, table, bits):
        permutation = ''
        for i in range(0, bits):
            permutation = permutation + text[table[i] - 1]
        return permutation

    def process_key(self, key):
        key = self.parse_key(key)
        key = key.encode().hex()
        key = self.hextobin(key)

        key = self.permutasi(key, self.key_permutation, len(self.key_permutation))
        kiri = key[0:int(len(self.key_permutation) / 2)]
        kanan = key[int(len(self.key_permutation) / 2):len(self.key_permutation)]

        keys = []
        for i in range(0, len(self.shift_bit)):
            kiri = self.shift_left(kiri, self.shift_bit[i])
            kanan = self.shift_left(kanan, self.shift_bit[i])

            lr = kiri + kanan

            internal_key = self.permutasi(lr, self.permutasi_kompresi, len(self.permutasi_kompresi))

            keys.append(internal_key)
        return keys

    def parse_key(self, key):
        if len(key) > 8:
            return key[0:8]
        else:
            return key

    def xor(self, arr, key):
        ans = ''
        for i in range(len(arr)):
            if arr[i] == key[i]:
                ans = ans + '0'
            else:
                ans = ans + '1'
        return ans


# xx = DES()
# kunci = 'abcdefgh'
# # in_key = xx.process_key(kunci)
# ptex = b'akuanime'
# encr = xx.encrypt(kunci, ptex)
# decr = xx.decrypt(kunci, encr)
# print(xx.hextobin(encr.hex()))
# print(decr)
