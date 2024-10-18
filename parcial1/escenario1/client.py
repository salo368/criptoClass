import socket
from salsa import Salsa20Cipher

class Client:

    def __init__(self, port: int, server_ip: str, server_port: int):
        self.ip = self.__get_ip()
        self.port = port
        self.server_ip = server_ip
        self.server_port = server_port
        self.socket = None  # Socket will be created during connection
        self.connected = False
        self.cipher = None # cipher will be created after receiving the key
        print(f"Client ready to connect to {self.server_ip}:{self.server_port}")

    def run(self):
        """Loop to continuously send and receive messages."""
        try:
            self.__connect_socket()
            key = self.socket.recv(1024)
            print("Key received")
            self.cipher = Salsa20Cipher(key)
            while self.connected:
                # Sending message
                message = input("Enter message to send (or 'exit' to quit): ")
                if message.lower() == 'exit':
                    print("Closing connection.")
                    break
                self.__send_message(message)
                print("Waiting for message...")
                # Receiving message
                response = self.__receive_message()
                if response is None:
                    break
        finally:
            self.__close_connection()

    def __get_ip(self):
        return socket.gethostbyname(socket.gethostname())

    def __create_socket(self):
        if self.socket is None:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.ip, self.port))
            print(f"Socket created for client at {self.ip}:{self.port}")

    def __connect_socket(self):
        if not self.connected:
            self.__create_socket()
            try:
                self.socket.connect((self.server_ip, self.server_port))
                self.connected = True
                print(f"Connected to server at {self.server_ip}:{self.server_port}")
            except Exception as e:
                print(f"Error connecting to server: {e}")
                self.connected = False

    def __send_message(self, message: str):
        """Send an encrypted message to the server."""
        try:
            self.__connect_socket()
            if self.connected:
                encrypted_message = self.cipher.encrypt(message.encode())
                self.socket.sendall(encrypted_message)
                print(f"Sent encrypted message to {self.server_ip}:{self.server_port}")
        except Exception as e:
            print(f"Error sending message: {e}")

    def __receive_message(self):
        """Receive an encrypted message and decrypt it."""
        try:
            if self.connected:
                data = self.socket.recv(1024)
                if data:
                    decrypted_message = self.cipher.decrypt(data).decode()
                    print(f"Received message: {decrypted_message}")
                    return decrypted_message
                else:
                    print("No data received.")
                    return None
        except Exception as e:
            print(f"Error receiving message: {e}")
            return None

    def __close_connection(self):
        if self.socket:
            try:
                self.socket.close()
                self.connected = False
                print(f"Connection to {self.server_ip}:{self.server_port} closed.")
            except Exception as e:
                print(f"Error closing the connection: {e}")

if __name__ == "__main__":
    client = Client(port=8081, server_ip="192.168.1.13", server_port=8080)
    client.run()
