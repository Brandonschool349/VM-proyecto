import socket
import ssl
import json
import hashlib

# Configura la IP y puerto del servidor al que quieres conectarte
HOST = '192.168.10.11'  # IP de SrvA
PORT = 5000

# Crear contexto SSL (ignorar verificaci  n de certificado para pruebas)
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

# Conectar y enviar credenciales
with socket.create_connection((HOST, PORT)) as sock:
    with context.wrap_socket(sock, server_hostname=HOST) as ssock:
        credenciales = {
            "user": "admin",
            "hash": hashlib.sha256("admin123".encode()).hexdigest()
        }
        ssock.send(json.dumps(credenciales).encode())
        print(ssock.recv(1024).decode())  # Deber  a imprimir AUTH_OK

        # Enviar comando "monitor"
        ssock.send(b"monitor")
        print(ssock.recv(1024).decode())

        # Cerrar conexi  n
        ssock.send(b"exit")



