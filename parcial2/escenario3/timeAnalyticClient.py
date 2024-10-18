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


tamanos = np.linspace(1, 4000, 100, dtype=int)
tiempos_salsa = []
tiempos_aes = []
tiempos_rsa = []
tiempos_elgamal = []


for tamano in tamanos:
    print(f'Para {tamano} bytes')
    tiempos = run_client(tamano)
    tiempos_salsa.append(tiempos[0])
    tiempos_aes.append(tiempos[1])
    tiempos_rsa.append(tiempos[2])
    tiempos_elgamal.append(tiempos[3])


plt.figure(figsize=(10, 6))
plt.plot(tamanos, tiempos_salsa, label='Salsa', color='blue')
plt.plot(tamanos, tiempos_aes, label='AES', color='green')
plt.plot(tamanos, tiempos_rsa, label='RSA', color='red')
plt.plot(tamanos, tiempos_elgamal, label='ElGamal', color='orange')


plt.title('Tiempo de Ejecución por Tamaño de Mensaje')
plt.xlabel('Tamaño del Mensaje en Bytes')
plt.ylabel('Tiempo de Ejecución (s)')
plt.legend()
plt.grid()

plt.show()
