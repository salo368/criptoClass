import socket
import time
from salsa import Salsa20Cipher
from cbc import AESCipherCBC
from rsaOaep import RSA_OAEPCipher
from elGamal import elGamalCipher
import pickle
import os
import matplotlib.pyplot as plt
import numpy as np


def run_client(message_lenght):
    server_ip = "192.168.1.7"  
    server_port = 8080

    avg_times = []
    
    for algo_index in range(4):
        total_time = 0
        keys = None

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((server_ip, server_port))

            bytes_data = algo_index.to_bytes(4, byteorder='big')
            client_socket.sendall(bytes_data)

            if algo_index == 0:
                key = client_socket.recv(2048)
                cipher = Salsa20Cipher(key)
            elif algo_index == 1:
                key = client_socket.recv(2048)
                cipher = AESCipherCBC(key)
            elif algo_index == 2:
                key = client_socket.recv(2048)
                keys = pickle.loads(key)
                cipher = RSA_OAEPCipher()
            elif algo_index == 3:
                key = client_socket.recv(2048)
                keys = pickle.loads(key)
                cipher = elGamalCipher()

            message = os.urandom(message_lenght)
            for i in range(5):
                start_time = time.time()

                if algo_index == 0:
                    enc = cipher.encrypt(message)
                elif algo_index == 1:
                    enc = cipher.encrypt(message)
                elif algo_index == 2:
                    enc = cipher.encrypt(message, keys)
                elif algo_index == 3:
                    enc = cipher.encrypt(message, keys[0], keys[1], keys[2])

                client_socket.sendall(enc)

                data = client_socket.recv(1024)
                end_time = time.time()

                elapsed_time = end_time - start_time
                total_time += elapsed_time

                #print(f"Algoritmo {algo_index}, Intento {i + 1}: {elapsed_time:.6f} segundos")

            avg_time = total_time / 5
            avg_times.append(avg_time)
            #print(f"Algoritmo {algo_index} - Tiempo promedio de 5 intentos: {avg_time:.6f} segundos")


    print("\nTiempos promedios de cada algoritmo:")
    print(f"Salsa: {avg_times[0]:.6f} segundos")
    print(f"AES: {avg_times[1]:.6f} segundos")
    print(f"RSA: {avg_times[2]:.6f} segundos")
    print(f"ElGamal: {avg_times[3]:.6f} segundos")

    return avg_times


sizes = np.linspace(1, 4000, 20, dtype=int)
salsa_times = []
aes_times = []
rsa_times = []
elgamal_times = []

for size in sizes:
    print(f'For {size} bytes')
    times = run_client(size)
    salsa_times.append(times[0])
    aes_times.append(times[1])
    rsa_times.append(times[2])
    elgamal_times.append(times[3])

plt.figure(figsize=(10, 6))
plt.plot(sizes, salsa_times, label='Salsa', color='blue')
plt.plot(sizes, aes_times, label='AES', color='green')
plt.plot(sizes, rsa_times, label='RSA', color='red')
plt.plot(sizes, elgamal_times, label='ElGamal', color='orange')

plt.title('Execution Time by Message Size')
plt.xlabel('Message Size in Bytes')
plt.ylabel('Execution Time (s)')
plt.legend()
plt.grid()

plt.show()
