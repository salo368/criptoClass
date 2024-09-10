import socket
from salsa import Salsa20Cipher

class Server:

    def __init__(self, port: int):
        self.ip = self.__get_ip()
        self.port = port
        self.socket = self.__create_socket()
        self.cipher = Salsa20Cipher()
        print(f"Server started, listening on {self.ip}:{self.port}")

    def run(self):
        """Main server loop to accept and handle incoming client connections."""
        try:
            while True:
                print(f"Waiting for a connection on {self.ip}:{self.port}...")
                conn, addr = self.socket.accept()  # Accept a new client connection
                self.__handle_client(conn, addr)     # Handle the client in a dedicated method
        except KeyboardInterrupt:
            print("Server shutting down.")
        finally:
            self.__close_server()

    def __get_ip(self):
        """Get the server's local IP address."""
        return socket.gethostbyname(socket.gethostname())

    def __create_socket(self):
        """Create and bind the server socket to listen for incoming connections."""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.ip, self.port))
        server_socket.listen(5)  # Can handle up to 5 simultaneous connections
        print(f"Socket created and bound to {self.ip}:{self.port}")
        return server_socket

    def __handle_client(self, conn, addr):
        """Handle communication with a connected client."""
        with conn:
            print(f"Connected by {addr}")
            conn.sendall(self.cipher.key)
            print("Key sent")
            while True:
                print("Waiting for message...")
                try:
                    data = conn.recv(1024)
                    if not data:
                        print(f"Client {addr} disconnected.")
                        break  # Client disconnected

                    # Decrypt the received message
                    decrypted_message = self.cipher.descifrar(data).decode()
                    print(f"Received from {addr}: {decrypted_message}")

                    # Optionally send a response to the client
                    response = input("Response: ")
                    encrypted_response = self.cipher.cifrar(response.encode())
                    conn.sendall(encrypted_response)

                except Exception as e:
                    print(f"Error handling client {addr}: {e}")
                    break

    def __close_server(self):
        """Close the server socket properly."""
        if self.socket:
            try:
                self.socket.close()
                print("Server socket closed.")
            except Exception as e:
                print(f"Error closing the server socket: {e}")

if __name__ == "__main__":
    server = Server(port=8080)
    server.run()
