import json
import socket

from diffie_hellman import DiffieHellmanProtocol
from salsa import Salsa20Cipher

class Client:

    def __init__(self, port: int, server_ip: str, server_port: int):
        self.salsa = Salsa20Cipher()

        self.server_ip = server_ip
        self.server_port = server_port

        self.ip = self.__get_ip()
        self.port = port
        self.socket = None  # Socket will be created during connection
        self.connected = False
    
        print(f"Client ready to connect to {self.server_ip}:{self.server_port}")

    def __get_ip(self):
        """Get the client's local IP address"""
        return socket.gethostbyname(socket.gethostname())

    def __create_socket(self):
        if self.socket is None:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.ip, self.port))
            print(f"Socket created and bound to {self.ip}:{self.port}")

    def __connect_socket(self):
        if not self.connected:
            self.__create_socket()
            try:
                self.socket.connect((self.server_ip, self.server_port))
                self.connected = True
                print(f"Connected to server at {self.server_ip}:{self.server_port}")
            except Exception as e:
                print(f"Error connecting to server: {e}")

    def __send_message(self, message: str):
        """Send an encrypted message to the server."""
        try:
            self.__connect_socket()
            if self.connected:
                encrypted_message = self.salsa.encrypt(message.encode())
                self.socket.sendall(encrypted_message)
                print(f"Sent encrypted message to {self.server_ip}:{self.server_port}")
        except Exception as e:
            self.connected = False
            print(f"Error sending message: {e}")

    def __receive_message(self):
        """Receive and decrypt a message from the server."""
        try:
            if self.connected:
                data = self.socket.recv(5120)
                return data
        except Exception as e:
            print(f"Error receiving message: {e}")
            self.connected = False
            return None

    def __handle_exchange(self, exchange_data: str):
        """Handle Diffie-Hellman key exchange with the server."""
        print("\n\n############### KEY EXCHANGE ###############\n")

        dh_json = exchange_data[9:]

        server_public_key = json.loads(dh_json)["pk"]
        print(f"Server public key:", server_public_key)
        
        dh = DiffieHellmanProtocol.from_json(dh_json)
        print(dh)

        # Send the client's public key to the server
        client_public_key = dh.pk
        self.socket.sendall(str(client_public_key).encode())
        print(f"Client public key sent to server")
        
        shared_secret = dh.get_shared_secret(server_public_key)
        print(f"Shared secret:", shared_secret)

        self.salsa.key = str(shared_secret).encode()
        print(f"Symmetric key:", self.salsa)

    def __close_connection(self):
        if self.socket is not None:
            try:
                self.socket.close()
                print(f"Connection to {self.server_ip}:{self.server_port} closed.")
            except Exception as e:
                print(f"Error closing the connection: {e}")

    def run(self):
        """Loop to continuously send and receive messages."""
        try:
            self.__connect_socket()
            print("Waiting for server params and public key...")
            response = self.socket.recv(5120)
            self.__handle_exchange(response.decode())

            while self.connected:

                # Sending message
                message = input("\nEnter message to send (or 'exit' to quit): ")
                if message.lower() == 'exit':
                    print("Closing connection.")
                    break
                self.__send_message(message)

                print("Waiting for message...")
                # Receiving message
                response = self.__receive_message()
                if not response:
                    break

                response_decoded = response.decode(errors="ignore")
                if response_decoded.startswith("EXCHANGE"):
                    self.__handle_exchange(response_decoded)
                
                else:
                    decrypted_message = self.salsa.decrypt(response).decode()
                    print(f"Received from ({self.server_ip}, {self.server_port}): {decrypted_message}")
                
        except KeyboardInterrupt:
            print("Client shutting down")
        
        finally:
            self.__close_connection()

if __name__ == "__main__":
    client = Client(port=8081, server_ip="192.168.1.15", server_port=8080)
    client.run()
