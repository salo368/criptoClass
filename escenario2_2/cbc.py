from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

class AESCipherCBC:
    
    def __init__(self, key: bytes = get_random_bytes(32), block_size: int = 16):

        self.key = key 
        self.block_size = block_size

    def encrypt(self, data: bytes) -> bytes:

        iv = get_random_bytes(16)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        padded_data = pad(data, self.block_size)
        encrypted_data = cipher.encrypt(padded_data)

        return iv + encrypted_data
    
    def decrypt(self, iv_encrypted_data: bytes) -> bytes:

        iv = iv_encrypted_data[:16]

        encrypted_data = iv_encrypted_data[16:]
        decipher = AES.new(self.key, AES.MODE_CBC, iv)
        padded_data = decipher.decrypt(encrypted_data)
        data = unpad(padded_data, self.block_size)
        return data
