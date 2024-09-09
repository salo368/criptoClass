import socket
import argparse

class CriptoConnection:
    def __init__(self, port):
        self.port = port
        self.ip = self.get_ip_address()

    def get_ip_address(self):
        try:
            ip = socket.gethostbyname(socket.gethostname())
        except Exception as e:
            print(f"Error getting IP address: {e}")
            ip = "127.0.0.1"  # Fallback to localhost
        return ip

    def awaitMessage(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.ip, self.port))
            server_socket.listen(1)
            print(f"Listening on {self.ip}:{self.port}")
            conn, addr = server_socket.accept()
            with conn:
                print(f"Connected by {addr}")
                data = conn.recv(1024)
                if data:
                    print(f"Received message: {data.decode('utf-8')}")
                    return data.decode('utf-8')
                else:
                    print("No data received.")
                    return None

    def stayAwaitMessage(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.ip, self.port))
            server_socket.listen(1)
            print(f"Listening on {self.ip}:{self.port}")

            while True:
                conn, addr = server_socket.accept()
                with conn:
                    print(f"Connected by {addr}")
                    data = conn.recv(1024)
                    if data:
                        print(f"Received message: {data.decode('utf-8')}")
                    else:
                        print("No data received.")

    def sendMessage(self, port, ip, message):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((ip, port))
                client_socket.sendall(message.encode('utf-8'))
                print(f"Sent message: {message} to {ip}:{port}")
        except Exception as e:
            print(f"Error sending message: {e}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CriptoConnection: send or receive messages.")
    parser.add_argument("mode", choices=["await", "send", "stayawait"], help="Mode of operation: 'await' to receive once, 'send' to send, 'stayawait' to stay awaiting multiple messages.")
    parser.add_argument("port", type=int, help="Port to use.")
    parser.add_argument("ip", nargs="?", help="IP address to send message to (only required in send mode).")
    parser.add_argument("message", nargs="?", help="Message to send (only required in send mode).")

    args = parser.parse_args()

    cripto_conn = CriptoConnection(args.port)

    if args.mode == "await":
        cripto_conn.awaitMessage()
    elif args.mode == "stayawait":
        cripto_conn.stayAwaitMessage()
    elif args.mode == "send":
        if not args.ip or not args.message:
            print("IP address and message are required in send mode.")
        else:
            cripto_conn.sendMessage(args.port, args.ip, args.message)

# Comandos para uso:
# Await: python cripto.py await 8080 (puerto de recepción)
# - python cripto.py await 8080
# Await: python cripto.py await 8080 (puerto de recepción)
# - python cripto.py stayawait 8080
# Send: python cripto.py send 8080 (puerto de envío) 192.168.1.2 (ip de envío) "Hola mundo" (Mensaje)
# - python cripto.py send 8080 192.168.1.2 "Hola mundo"