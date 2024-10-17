import json
import socket
import os

from diffie_hellman import DiffieHellmanProtocol
from salsa import Salsa20Cipher

class Server:

    def __init__(self, port: int):
        self.diffie_hellman_cases = self.__get_diffie_hellman_cases()
        self.salsa = Salsa20Cipher()

        self.port = port
        self.ip = self.__get_ip()
        self.socket = self.__create_socket()

    def run(self):
        """Main server loop to accept and handle incoming client connections"""
        try:
            print(f"Server started, listening on {self.ip}:{self.port}")
            while True:
                print(f"Waiting for a connection on {self.ip}:{self.port}...")
                # Accept a new client connection
                conn, addr = self.socket.accept()
                # Handle the client in a dedicated method
                try:
                    self.__handle_client(conn, addr)
                except ConnectionResetError as e:
                    print(f"\nError: {e}", addr)
        except KeyboardInterrupt:
            print("Server shutting down")
        finally:
            self.__close_server()  
    
    def __get_diffie_hellman_cases(self) -> list[DiffieHellmanProtocol]:
        """Create a list that contains all the cases in parameters.json"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, "parameters.json")
        with open(file_path) as f:
            parameters_sets = json.load(f)["parameters"]
        return [DiffieHellmanProtocol(**parameters) for parameters in parameters_sets]
    
    def __get_ip(self) -> str:
        """Get the server's local IP address"""
        return socket.gethostbyname(socket.gethostname())
    
    def __create_socket(self) -> socket.socket:
        """Create and bind the server socket to listen for incoming connections"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.ip, self.port))
        server_socket.listen(5)
        print(f"Socket created and bound to {self.ip}:{self.port}")
        return server_socket
    
    def __receive_message(self, conn: socket.socket) -> bytes:
        message = conn.recv(4096)
        if not message:
            raise ConnectionResetError("Client disconnected")
        return message
    
    def __receive_decrypt_message(self, conn: socket.socket) -> str:
        """Receive the encrypted message and decrypt it"""
        encrypted_message = self.__receive_message(conn)
        decrypted_message = self.salsa.decrypt(encrypted_message).decode()
        return decrypted_message
    
    def __encrypt_send_message(self, conn: socket.socket, plain_message: str):
        """Encrypts the message and sends it to the client"""
        encrypted_message = self.salsa.encrypt(plain_message.encode())
        conn.sendall(encrypted_message)

    def __key_exchange(self, conn: socket.socket, dh: DiffieHellmanProtocol) -> int:
        """Handle Diffie-Hellman key exchange and return the shared secret"""
        conn.sendall(b"EXCHANGE " + bytes(dh))
        print("Parameters and public key sent to client")

        print("Waiting for client public key...")
        client_public_key = int(self.__receive_message(conn).decode())
        print("Client public key:", client_public_key)

        shared_secret = dh.get_shared_secret(client_public_key)
        print("Shared secret:", shared_secret)
        return shared_secret    

    def __handle_client(self, conn: socket.socket, addr: tuple[str, int]):
        """Handle communication with a connected client."""
        with conn:
            print(f"Client {addr} disconnected.")

            print(f"Connected by", addr)

            for i, dh in enumerate(self.diffie_hellman_cases, 1):
                print(f"\n\n############### CASE {i} ###############\n")
                print(dh)

                shared_secret = self.__key_exchange(conn, dh)

                self.salsa.key = str(shared_secret).encode()
                print("Symmetric key:", self.salsa)

                while True:
                    print("\nWaiting for message...")
                    
                    decrypted_message = self.__receive_decrypt_message(conn)
                    print(f"Received from {addr}: {decrypted_message}")

                    # Response to the client
                    response = input("Response (or 'next' or 'exit'): ")
                    # Stop handling client
                    if response.lower() == "exit":
                        return
                    # Next key exchange
                    if response.lower() == "next":
                        break

                    self.__encrypt_send_message(conn, response)
            else:
                print("All cases completed, closing connection with client\n")

    def __close_server(self):
        """Close the server socket properly."""
        if self.socket:
            try:
                self.socket.close()
                print("Server socket closed.")
            except Exception as e:
                print("Error closing the server socket:", e)

if __name__ == "__main__":
    server = Server(port=8080)
    server.run()
