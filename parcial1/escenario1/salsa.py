from Crypto.Cipher import Salsa20
from Crypto.Random import get_random_bytes

class Salsa20Cipher:

    def __init__(self, key: bytes = get_random_bytes(32)):
        # 32 bytes key
        self.key = key

    def generate_new_key(self):
        self.key = get_random_bytes(32)

    def encrypt(self, data: bytes) -> bytes:
        nonce = get_random_bytes(8)
        cipher = Salsa20.new(key=self.key, nonce=nonce)
        encrypted_data = cipher.encrypt(data)
        return nonce + encrypted_data

    def decrypt(self, nonce_encrypted_data: bytes) -> bytes:
        nonce = nonce_encrypted_data[:8]
        encrypted_data = nonce_encrypted_data[8:]
        decipher = Salsa20.new(key=self.key, nonce=nonce)
        data = decipher.decrypt(encrypted_data)
        return data

