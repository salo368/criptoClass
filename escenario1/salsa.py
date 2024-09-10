from Crypto.Cipher import Salsa20
from Crypto.Random import get_random_bytes

class Salsa20Cipher:

    def __init__(self, key: bytes = get_random_bytes(32)):
        # clave de 32 bytes
        self.key = key

    def cifrar(self, data: bytes) -> bytes:
        nonce = get_random_bytes(8)
        cipher = Salsa20.new(key=self.key, nonce=nonce)
        encrypted_data = cipher.encrypt(data)
        return nonce + encrypted_data

    def descifrar(self, nonce_encrypted_data: bytes) -> bytes:
        nonce = nonce_encrypted_data[:8]
        encrypted_data = nonce_encrypted_data[8:]
        decipher = Salsa20.new(key=self.key, nonce=nonce)
        data = decipher.decrypt(encrypted_data)
        return data
