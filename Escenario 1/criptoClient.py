import socket
from salsa import Salsa20Cipher as salsa20

class CriptoConnection:
    def __init__(self, port):
        self.port = port
        self.ip = self.get_ip_address()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crea el socket en el constructor
        self.socket.bind((self.ip, self.port))  # Asocia el socket con la dirección IP y el puerto
        self.socket.listen(1)  # Escucha por conexiones entrantes
        print(f"Socket created and listening on {self.ip}:{self.port}")

    def get_ip_address(self):
        try:
            ip = socket.gethostbyname(socket.gethostname())  # Obtiene la IP del host
        except Exception as e:
            print(f"Error getting IP address: {e}")
            ip = "127.0.0.1"  # IP localhost por defecto
        return ip

    def awaitMessage(self):
        print(f"Waiting for a connection on {self.ip}:{self.port}")
        conn, addr = self.socket.accept()  # Acepta una conexión entrante
        with conn:
            print(f"Connected by {addr}")
            data = conn.recv(1024)  # Recibe el mensaje
            if data:
                return data  # Retorna el mensaje decodificado
            else:
                print("No data received.")
                return None

    def sendMessage(self, ip, port, message):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((ip, port))  # Conecta al socket remoto
                client_socket.sendall(message)  # Envía el mensaje
                print(f"Sent message: {message} to {ip}:{port}")
        except Exception as e:
            print(f"Error sending message: {e}")

    def endSocket(self):
        try:
            self.socket.close()  # Cierra el socket
            print("Socket closed.")
        except Exception as e:
            print(f"Error closing socket: {e}")


server_port=8080
server_ip="10.20.8.67"

conexion = CriptoConnection(8080)

conexion.sendMessage(server_ip,server_port,"Mensaje Test".encode("utf-8"))

key=conexion.awaitMessage()

salsa = salsa20(key)

while True:
    
    menssage=input()
    conexion.sendMessage(server_ip,server_port,salsa.cifrar(menssage.encode("utf-8")))

    menssage_out=conexion.awaitMessage()
    print(salsa.descifrar(menssage_out).decode("utf-8"))