import socket
import ssl
import threading

# --- CONFIGURACIÓN DE RED ---
MID_HOST = '192.168.10.20' # IP del Middleware variable para facilitar cambios futuros
MID_PORT = 6000
TARGET_HOST = '192.168.10.10' # IP del Servidor Real (SrvA) al que el Middleware se conectará de forma segura variando para facilitar cambios futuros
TARGET_PORT = 5000

def manejar_trafico(origen, destino):
    while True:
        try:
            datos = origen.recv(4096)
            if not datos:
                break
            destino.send(datos)
        except:
            break

def iniciar_middleware():
    # Contexto para recibir al cliente
    context_server = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context_server.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

    # Contexto para conectarse al SrvA
    context_client = ssl.create_default_context()
    context_client.check_hostname = False
    context_client.verify_mode = ssl.CERT_NONE

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as mid_sock:
        mid_sock.bind((MID_HOST, MID_PORT))
        mid_sock.listen(5)
        print(f"[*] Middleware BLINDADO escuchando en {MID_HOST}:{MID_PORT}")

        with context_server.wrap_socket(mid_sock, server_side=True) as cliente_sock:
            conn_cliente, addr = cliente_sock.accept()
            print(f"[+] Cliente conectado desde {addr}")

            # Conectar al Servidor Real (SrvA)
            srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn_srv = context_client.wrap_socket(srv_sock, server_hostname=TARGET_HOST)
            conn_srv.connect((TARGET_HOST, TARGET_PORT))
            print(f"[+] Túnel seguro establecido con SrvA ({TARGET_HOST})")

            # Hilos para tráfico bidireccional
            hilo_ida = threading.Thread(target=manejar_trafico, args=(conn_cliente, conn_srv))
            hilo_vuelta = threading.Thread(target=manejar_trafico, args=(conn_srv, conn_cliente))
            
            hilo_ida.start()
            hilo_vuelta.start()

if __name__ == "__main__":
    iniciar_middleware()