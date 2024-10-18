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
        ip_address = s.getsockname()[0]
    except Exception:
        ip_address = "127.0.0.1"
    finally:
        s.close()
    return ip_address

def run_server():
    server_ip = get_ip()
    server_port = 8080

    rsa_cipher = RSA_OAEPCipher()
    elgamal_cipher = elGamalCipher()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((server_ip, server_port))
        server_socket.listen(1)
        print(f"Server listening on {server_ip}:{server_port}")

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"Connection from {addr}")

                data = conn.recv(4)
                algo = int.from_bytes(data, byteorder='big')

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

                    if algo == 0:
                        decrypted_message = salsa20_cipher.decrypt(data)
                    elif algo == 1:
                        decrypted_message = aes_cipher.decrypt(data)
                    elif algo == 2:
                        decrypted_message = rsa_cipher.decrypt(data)
                    elif algo == 3:
                        decrypted_message = elgamal_cipher.decrypt(data)

                    conn.sendall(b"Message received")

if __name__ == "__main__":
    run_server()
