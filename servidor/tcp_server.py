import socket
import ssl
import json
import psutil
import subprocess
import hashlib

# --- CONFIGURACIÓN DE RED (Desafío 2 resuelto) ---
HOST = '192.168.10.10' #HOST del Servidor Real (SrvA) variable para facilitar cambios futuros
PORT = 5000

# Base de datos simulada de usuarios (Contraseña real: "admin123")
USUARIOS_VALIDOS = {
    "admin": hashlib.sha256("admin123".encode()).hexdigest()
}

def ejecutar_comando(comando):
    if comando == 'monitor':
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "ram_percent": psutil.virtual_memory().percent
        }
    elif comando == 'list':
        procesos = []
        for p in psutil.process_iter(['pid', 'name']):
            procesos.append(p.info)
            if len(procesos) >= 15: # Limitamos a 15 para no saturar la pantalla
                break
        return {"procesos": procesos}
    else:
        return {"error": "Comando no reconocido"}

def iniciar_servidor():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen(5)
        print(f"[*] Servidor escuchando de forma SEGURA (TLS/SSL) en {HOST}:{PORT}")

        with context.wrap_socket(sock, server_side=True) as ssock:
            conn, addr = ssock.accept()
            print(f"[+] Conexión segura establecida con {addr}")
            
            # Fase de Autenticación
            credenciales = json.loads(conn.recv(1024).decode())
            if USUARIOS_VALIDOS.get(credenciales['user']) == credenciales['hash']:
                conn.send(b"AUTH_OK")
                print("[!] Autenticación exitosa.")
                
                # Bucle de comandos
                while True:
                    data = conn.recv(1024).decode()
                    if not data or data == 'exit':
                        break
                    respuesta = ejecutar_comando(data)
                    conn.send(json.dumps(respuesta).encode())
            else:
                conn.send(b"AUTH_FAIL")
                print("[-] Intento de acceso denegado.")

if __name__ == "__main__":
    iniciar_servidor()