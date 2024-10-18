from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA1
from typing import List
import pickle

class RSA_OAEPCipher:
    
    def __init__(self):
        self.key_size = 1024 
        key = RSA.generate(self.key_size)  
        self.private_key = key.export_key()
        self.public_key = key.publickey().export_key()
        self.max_length = self.key_size // 8 - 2 * SHA1.digest_size - 2  

    def encrypt(self, data: bytes, public_key) -> bytes:
        cipher = PKCS1_OAEP.new(RSA.import_key(public_key))
        blocks = [data[i:i + self.max_length] for i in range(0, len(data), self.max_length)]
        encrypted_blocks = [cipher.encrypt(block) for block in blocks]
        return b''.join(encrypted_blocks)

    def decrypt(self, encrypted_data: bytes) -> bytes:
        cipher = PKCS1_OAEP.new(RSA.import_key(self.private_key))
        block_size = self.key_size // 8

        encrypted_blocks = [encrypted_data[i:i + block_size] for i in range(0, len(encrypted_data), block_size)]
        decrypted_data = b''.join(cipher.decrypt(block) for block in encrypted_blocks)
        return decrypted_data


# ALICE = RSA_OAEPCipher()
# BOB = RSA_OAEPCipher()

# bob_public_key = BOB.public_key

# alice_public_key = ALICE.public_key

# serialized_data = pickle.dumps(bob_public_key)

# print(serialized_data)

# texto = 'La creatividad es una de las capacidades humanas más valiosas, y su influencia se extiende a prácticamente todos los ámbitos de la vida. A menudo asociada con las artes, la creatividad es en realidad un pilar fundamental en el desarrollo de cualquier disciplina, desde la ingeniería hasta la ciencia, pasando por los negocios y la educación. En un mundo cada vez más competitivo y globalizado, la creatividad ha dejado de ser solo una ventaja; se ha convertido en una necesidad para quienes buscan destacar y generar un impacto duradero.'
# enc = ALICE.encrypt(texto.encode(), bob_public_key)

# mensage = BOB.decrypt(enc)
# print(mensage.decode())
