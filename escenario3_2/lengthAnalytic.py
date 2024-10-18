import matplotlib.pyplot as plt
from Crypto.Random import get_random_bytes
from cbc import AESCipherCBC
from salsa import Salsa20Cipher
from elGamal import elGamalCipher
from rsaOaep import RSA_OAEPCipher
import numpy as np

salsa20_cipher = Salsa20Cipher()
rsa_cipher = RSA_OAEPCipher()
elgamal_cipher = elGamalCipher()
aes_cipher = AESCipherCBC()

message_sizes = np.linspace(1, 10000, 100, dtype=int).tolist()


salsa20_sizes = []
rsa_sizes = []
elgamal_sizes = []
aes_sizes = []

for size in message_sizes:
    message = get_random_bytes(size)

    # Cifrado con Salsa20
    encrypted_salsa20 = salsa20_cipher.encrypt(message)
    salsa20_sizes.append(len(encrypted_salsa20))

    # Cifrado con RSA
    encrypted_rsa = rsa_cipher.encrypt(message, rsa_cipher.public_key)
    rsa_sizes.append(len(encrypted_rsa))

    # Cifrado con ElGamal
    encrypted_elgamal = elgamal_cipher.encrypt(message, elgamal_cipher.public_key, elgamal_cipher.p, elgamal_cipher.g)
    elgamal_sizes.append(len(encrypted_elgamal))

    # Cifrado con AES
    encrypted_aes = aes_cipher.encrypt(message)
    aes_sizes.append(len(encrypted_aes))

print("Tamaños de mensajes originales (bytes):", message_sizes)
print("Tamaños de mensajes cifrados con Salsa20:", salsa20_sizes)
print("Tamaños de mensajes cifrados con RSA-OAEP:", rsa_sizes)
print("Tamaños de mensajes cifrados con ElGamal:", elgamal_sizes)
print("Tamaños de mensajes cifrados con AES:", aes_sizes)

plt.figure(figsize=(10, 6))

plt.plot(message_sizes, rsa_sizes, label="RSA-OAEP")
plt.plot(message_sizes, elgamal_sizes, label="ElGamal")
plt.plot(message_sizes, aes_sizes, label="AES-CBC")
plt.plot(message_sizes, salsa20_sizes, label="Salsa20")

plt.xlabel("Tamaño del mensaje original (bytes)")
plt.ylabel("Tamaño del mensaje cifrado (bytes)")
plt.title("Crecimiento del tamaño del mensaje cifrado según el algoritmo")
plt.legend()
plt.grid(True)
plt.show()
