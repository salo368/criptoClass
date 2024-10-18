import socket
import time
from salsa import Salsa20Cipher
from cbc import AESCipherCBC
from rsaOaep import RSA_OAEPCipher
from elGamal import elGamalCipher
import pickle
import os

def run_client():
    server_ip = "192.168.1.7"  
    server_port = 8080

    avg_times = []
    algorithms = [Salsa20Cipher, AESCipherCBC, RSA_OAEPCipher, elGamalCipher]

    for algo_index in range(4):
        total_time = 0
        keys = None

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((server_ip, server_port))

            # Recibir la clave del servidor según el algoritmo
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

            message = os.urandom(2048)
            for i in range(5):
                start_time = time.time()

                # Encriptar el mensaje
                if algo_index == 0:
                    enc = cipher.encrypt(message)
                elif algo_index == 1:
                    enc = cipher.encrypt(message)
                elif algo_index == 2:
                    enc = cipher.encrypt(message, keys)
                elif algo_index == 3:
                    enc = cipher.encrypt(message, keys[0], keys[1], keys[2])

                # Enviar el mensaje cifrado al servidor
                client_socket.sendall(enc)

                # Recibir la respuesta del servidor
                data = client_socket.recv(1024)
                end_time = time.time()

                elapsed_time = end_time - start_time
                total_time += elapsed_time

                print(f"Algoritmo {algo_index}, Intento {i + 1}: {elapsed_time:.6f} segundos")

            avg_time = total_time / 5
            avg_times.append(avg_time)
            print(f"Algoritmo {algo_index} - Tiempo promedio de 5 intentos: {avg_time:.6f} segundos")

            # Notificar al servidor que se completaron las pruebas para este algoritmo
            client_socket.sendall(f"FIN_ALG {algo_index}".encode())

    print("\nTiempos promedios de cada algoritmo:")
    for i, avg in enumerate(avg_times):
        print(f"Algoritmo {i}: {avg:.6f} segundos")

run_client()
