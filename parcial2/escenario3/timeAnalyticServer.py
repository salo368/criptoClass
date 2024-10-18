import socket
from salsa import Salsa20Cipher
from cbc import AESCipherCBC
from rsaOaep import RSA_OAEPCipher
from elGamal import elGamalCipher
import pickle

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception as e:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def run_server():
    server_ip = get_ip()
    server_port = 8080
    salsa20_cipher = None
    aes_cipher = None
    rsa_cipher = RSA_OAEPCipher()
    elgamal_cipher = elGamalCipher()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((server_ip, server_port))
        server_socket.listen(1)
        print(f"Servidor escuchando en {server_ip}:{server_port}")

        algo = 0  # Comienza con el primer algoritmo

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"Conexión desde {addr}")

                # Enviar la clave según el algoritmo actual
                if algo == 0:
                    salsa20_cipher = Salsa20Cipher()
                    key = salsa20_cipher.key
                    conn.sendall(key)
                elif algo == 1:
                    aes_cipher = AESCipherCBC()
                    key = aes_cipher.key
                    conn.sendall(key)
                elif algo == 2:
                    key = pickle.dumps(rsa_cipher.public_key)
                    conn.sendall(key)
                elif algo == 3:
                    key = pickle.dumps((elgamal_cipher.public_key, elgamal_cipher.p, elgamal_cipher.g))
                    conn.sendall(key)

                for _ in range(5):
                    data = conn.recv(8192)
                    if not data:
                        break

                    # Procesar el mensaje cifrado
                    if algo == 0:
                        desc = salsa20_cipher.decrypt(data)
                    elif algo == 1:
                        desc = aes_cipher.decrypt(data)
                    elif algo == 2:
                        desc = rsa_cipher.decrypt(data)
                    elif algo == 3:
                        desc = elgamal_cipher.decrypt(data)
                    
                    conn.sendall(b"Mensaje recibido")
                    #print(desc)

                # Esperar un mensaje de control para cambiar el algoritmo
                control_msg = conn.recv(1024).decode()
                if control_msg.startswith("FIN_ALG"):
                    algo += 1  # Incrementar el índice del algoritmo para la siguiente conexión
                    print(f"Cambiando a algoritmo {algo}")

if __name__ == "__main__":
    run_server()
