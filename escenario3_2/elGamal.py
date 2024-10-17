from Crypto.PublicKey import ElGamal
from Crypto.Random import get_random_bytes
from Crypto.Math._IntegerCustom import IntegerCustom
import random
import math

class elGamalCipher:

    def __init__(self):
        key = ElGamal.generate(256, get_random_bytes)
        self.private_key = key.x
        self.public_key = key.y
        self.p = key.p 
        self.g = key.g 
    
    def encrypt(self, data: bytes):
        m = IntegerCustom(int.from_bytes(data, 'big'))
        
        blocks = []
        while m >= self.p:
            blocks.append(m % self.p)
            m = m // self.p
        blocks.append(m)
        blocks = blocks[::-1]  

        encrypted_blocks = []
        for block in blocks:

            num = random.randint(1, self.p - 1)
            while math.gcd(num, self.p) != 1:
                num = random.randint(1, self.p - 1)
            k = num

            v = pow(self.g, k, self.p)
            w = pow(self.public_key, k, self.p)
            c = (block * w) % self.p

            encrypted_blocks.append((c, v))
        
        return encrypted_blocks
            
    def decrypt(self, encrypted_blocks):
        decrypted_blocks = []
        
        for c, v in encrypted_blocks:

            w = pow(v, self.private_key, self.p)
            w_inv = pow(w, self.p - 2, self.p)   
            m = (c * w_inv) % self.p
            decrypted_blocks.append(m)
        
        m_total = IntegerCustom(0)
        for block in decrypted_blocks:
            m_total = m_total * self.p + block
        
        m_int = m_total._value
        return m_int.to_bytes((m_int.bit_length() + 7) // 8, 'big')


gamal = elGamalCipher()
# print(f'sk = {gamal.private_key}')
# print(f'pk = {gamal.public_key}')
# print(f'p = {gamal.p}')
# print(f'g = {gamal.g}')
texto = 'La creatividad es una de las capacidades humanas más valiosas, y su influencia se extiende a prácticamente todos los ámbitos de la vida. A menudo asociada con las artes, la creatividad es en realidad un pilar fundamental en el desarrollo de cualquier disciplina, desde la ingeniería hasta la ciencia, pasando por los negocios y la educación. En un mundo cada vez más competitivo y globalizado, la creatividad ha dejado de ser solo una ventaja; se ha convertido en una necesidad para quienes buscan destacar y generar un impacto duradero.'
enc = gamal.encrypt(texto.encode())
# print(enc)
mensage = gamal.decrypt(enc)
print(mensage.decode())



