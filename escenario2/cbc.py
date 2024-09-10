from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

class AESCipherCBC:
    
    def __init__(self, key: bytes, block_size: int = 16):
        # Clave de 16, 24 o 32 bytes (AES-128, AES-192, AES-256)
        self.key = key
        # Multiplo de 16
        self.block_size = block_size

    def cifrar(self, data: bytes) -> bytes:
        # Vector de inicializacion
        iv = get_random_bytes(16)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        padded_data = pad(data, self.block_size)
        encrypted_data = cipher.encrypt(padded_data)
        # Se adjunta el vector como los primeros 16 bytes
        return iv + encrypted_data
    
    def descifrar(self, iv_encrypted_data: bytes) -> bytes:
        # Se obtiene el vector de los primeros 16 bytes
        iv = iv_encrypted_data[:16]
        # El resto corresponde a la informacion cifrada
        encrypted_data = iv_encrypted_data[16:]
        decipher = AES.new(self.key, AES.MODE_CBC, iv)
        padded_data = decipher.decrypt(encrypted_data)
        data = unpad(padded_data, self.block_size)
        return data
