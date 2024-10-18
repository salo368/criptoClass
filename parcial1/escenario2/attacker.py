import socket
from padding_oracle import decrypt, base64_encode, base64_decode
from Crypto.Util.Padding import unpad

class PaddingOracleAttack:
    def __init__(self, server_ip, server_port, encrypted_message_hex):
        self.server_ip = server_ip
        self.server_port = server_port
        self.encrypted_message = bytes.fromhex(encrypted_message_hex)
        self.sock = None

    def connect_to_server(self):
        """Establish a connection to the server."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.server_ip, self.server_port))

    def close_connection(self):
        """Close the connection to the server."""
        if self.sock:
            self.sock.close()

    def send_message(self, message):
        """Send a message to the server and receive the response."""
        self.sock.sendall(b"NORESPONSE" + message)
        response = self.sock.recv(1024).decode()
        return response

    def oracle(self, ciphertext: bytes) -> bool:
        """Padding oracle function to query the server."""
        response = self.send_message(ciphertext)
        # Check server response for padding validity
        return "incorrect" not in response

    def perform_attack(self):
        """Perform the padding oracle attack on the encrypted message."""
        # Convert the encrypted message to base64 for compatibility with the library
        base64_ciphertext = base64_encode(self.encrypted_message)
        # Decrypt the message using the padding oracle library
        decrypted_message = decrypt(
            base64_decode(base64_ciphertext),
            block_size=16,
            oracle=self.oracle,
            num_threads=1
        )
        return decrypted_message

    def run(self):
        """Run the padding oracle attack process."""
        try:
            self.connect_to_server()
            # Perform the attack
            decrypted_message = self.perform_attack()
            decrypted_message = unpad(decrypted_message, 16)
            # Print the decrypted message
            print("Decrypted message:", decrypted_message.decode(errors='ignore').strip())
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.close_connection()

if __name__ == "__main__":
    # Attacker has access to intercepted encrypted message 
    encrypted_message_hex = "5f554034639b4aec336520081ff55a2a8cb0a255e233fbbe4feb7584676a9973"
    attacker = PaddingOracleAttack(server_ip="192.168.1.15", server_port=8080, encrypted_message_hex=encrypted_message_hex)
    attacker.run()
