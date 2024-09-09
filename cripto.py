import socket
import argparse

# Clase que maneja las conexiones a través de sockets
class CriptoConnection:
    def __init__(self, port):
        self.port = port  # Asigna el puerto que se va a utilizar para la conexión
        self.ip = self.get_ip_address()  # Obtiene la dirección IP del host

    # Método para obtener la dirección IP local del host
    def get_ip_address(self):
        try:
            ip = socket.gethostbyname(socket.gethostname())  # Obtiene la IP mediante el nombre del host
        except Exception as e:
            print(f"Error getting IP address: {e}") 
            ip = "127.0.0.1"  # Dirección IP por defecto (localhost)
        return ip

    # Método que espera recibir un mensaje una sola vez
    def awaitMessage(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.ip, self.port))  # Asocia el socket con la dirección IP y el puerto
            server_socket.listen(1)  # Escucha por conexiones entrantes, 1 significa una sola conexión
            print(f"Listening on {self.ip}:{self.port}")
            conn, addr = server_socket.accept()  # Acepta la conexión entrante
            with conn:
                print(f"Connected by {addr}")  
                data = conn.recv(1024)  # Recibe el mensaje hasta 1024 bytes
                if data:
                    print(f"Received message: {data.decode('utf-8')}")  # Decodifica e imprime el mensaje recibido
                    return data.decode('utf-8') 
                else:
                    print("No data received.")
                    return None

    # Método que espera múltiples mensajes de manera indefinida
    def stayAwaitMessage(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.ip, self.port))  # Asocia el socket con la dirección IP y el puerto
            server_socket.listen(1)  # Escucha por conexiones entrantes
            print(f"Listening on {self.ip}:{self.port}")

            while True:  
                conn, addr = server_socket.accept()  # Acepta conexiones entrantes
                with conn:
                    print(f"Connected by {addr}")
                    data = conn.recv(1024)  # Recibe el mensaje hasta 1024 bytes
                    if data:
                        print(f"Received message: {data.decode('utf-8')}")  # Decodifica e imprime el mensaje recibido
                    else:
                        print("No data received.")  

    # Método para enviar un mensaje a otro host
    def sendMessage(self, port, ip, message):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((ip, port))  # Establece la conexión con la IP y puerto destino
                client_socket.sendall(message.encode('utf-8'))  # Envía el mensaje codificado en UTF-8
                print(f"Sent message: {message} to {ip}:{port}")  
        except Exception as e:
            print(f"Error sending message: {e}")  


# Configuración para ejecutar el programa desde la línea de comandos
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CriptoConnection: send or receive messages.")# Argumentos de línea de comandos para elegir el modo de operación y otros parámetros
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