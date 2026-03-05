import socket
import ssl
import json
import hashlib

MID_HOST = '192.168.10.20'
MID_PORT = 6000

def iniciar_cliente():
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        with context.wrap_socket(sock, server_hostname=MID_HOST) as ssock:
            ssock.connect((MID_HOST, MID_PORT))
            
            print("=== SISTEMA DE GESTIÓN DISTRIBUIDA ===")
            usuario = input("Usuario: ")
            password = input("Contraseña: ")
            
            # Cifrado SHA-256 antes de enviar
            hash_pass = hashlib.sha256(password.encode()).hexdigest()
            credenciales = {"user": usuario, "hash": hash_pass}
            ssock.send(json.dumps(credenciales).encode())
            
            respuesta_auth = ssock.recv(1024).decode()
            
            if respuesta_auth == "AUTH_OK":
                print("\n[+] Acceso Concedido. Conexión Cifrada.")
                while True:
                    print("\n--- MENÚ ---")
                    print("1. list (Ver procesos)")
                    print("2. monitor (Ver CPU/RAM)")
                    print("3. exit (Salir)")
                    cmd = input("Comando> ")
                    
                    if cmd == 'exit' or cmd == '3':
                        ssock.send(b'exit')
                        break
                    elif cmd in ['list', '1']:
                        ssock.send(b'list')
                    elif cmd in ['monitor', '2']:
                        ssock.send(b'monitor')
                    else:
                        print("Comando inválido.")
                        continue
                        
                    resultado = ssock.recv(4096).decode()
                    # Formatear el JSON para que se vea bonito
                    print(json.dumps(json.loads(resultado), indent=4))
            else:
                print("\n[-] Acceso Denegado. Credenciales incorrectas.")

if __name__ == "__main__":
    iniciar_cliente()