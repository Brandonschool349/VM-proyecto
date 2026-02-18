import socket
import json

# Lista de servidores reales (SrvA, SrvC, etc.)
servers = ["192.168.50.10"]  # agrega más IP si quieres

LISTEN_HOST = '0.0.0.0'
LISTEN_PORT = 6000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((LISTEN_HOST, LISTEN_PORT))
    server.listen()
    print(f"Middleware escuchando en puerto {LISTEN_PORT}")

    while True:
        conn, addr = server.accept()
        with conn:
            try:
                data = conn.recv(1024).decode().strip()
                print(f"Cliente {addr} envió: {data}")

                if data == "servers":
                    # Discovery: devolvemos lista de servidores
                    conn.send(json.dumps(servers).encode())
                else:
                    # Reenviar al primer servidor (puedes hacer round-robin luego)
                    target_host = servers[0]
                    target_port = 5000
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as forward:
                        forward.connect((target_host, target_port))
                        forward.send(data.encode())
                        respuesta = forward.recv(4096)
                    conn.send(respuesta)

            except Exception as e:
                conn.send(json.dumps({"error": str(e)}).encode())