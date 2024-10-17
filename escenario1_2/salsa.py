from Crypto.Cipher import Salsa20
from Crypto.Hash import SHAKE256
from Crypto.Random import get_random_bytes

class Salsa20Cipher:

    def __init__(self, key: bytes = get_random_bytes(32)):
        # 32 bytes key
        self.__key = key

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

    def __str__(self) -> str:
        return self.key.hex()
    
    @property
    def key(self) -> bytes:
        return self.__key
    
    @key.setter
    def key(self, data: bytes):
        shake = SHAKE256.new()
        shake.update(data)
        self.__key = shake.read(32)
