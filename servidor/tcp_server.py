import socket
import ssl
import json
import psutil
import subprocess
import hashlib
import datetime
import os

HOST = '192.168.10.10' # IP del Servidor Real (SrvA) variable para facilitar cambios futuros
PORT = 5000

USUARIOS_VALIDOS = {
    "admin": hashlib.sha256("admin123".encode()).hexdigest()
}

procesos = {}

# Crear directorio de logs si no existe
LOG_DIR = "/opt/monitor_app/logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "server_audit.log")

def log_event(event):
    """Registra un evento en el log con timestamp"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {event}\n")

def list_logs():
    """Devuelve los últimos 50 registros del log"""
    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
            return lines[-50:]  # últimos 50 eventos
    except Exception as e:
        return [f"Error leyendo logs: {e}"]

def ejecutar_comando(cmd, client_addr):
    log_event(f"Comando recibido de {client_addr}: {cmd}")

    if cmd == "monitor":
        return {
            "cpu": psutil.cpu_percent(interval=1),
            "ram": psutil.virtual_memory().percent,
            "procesos_activos": len(procesos)
        }

    elif cmd == "list":
        salida = []
        for pid, proc in procesos.items():
            if proc.poll() is None:
                salida.append({
                    "pid": pid,
                    "cmd": " ".join(proc.args)
                })
        return salida

    elif cmd.startswith("run "):
        program = cmd[4:]
        try:
            proc = subprocess.Popen(program.split())
            procesos[proc.pid] = proc
            return {"status": f"Ejecutado {program}", "pid": proc.pid}
        except Exception as e:
            return {"error": str(e)}

    elif cmd.startswith("stop "):
        try:
            pid = int(cmd[5:])
            if pid in procesos:
                procesos[pid].terminate()
                return {"status": f"Proceso {pid} terminado"}
            else:
                return {"error": "PID no encontrado"}
        except Exception as e:
            return {"error": str(e)}

    elif cmd == "list_logs":
        return list_logs()

    else:
        return {"error": "Comando desconocido"}


def iniciar_servidor():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen(5)
        print(f"[*] Servidor TLS escuchando en {HOST}:{PORT}")
        log_event(f"Servidor iniciado en {HOST}:{PORT}")

        with context.wrap_socket(sock, server_side=True) as ssock:
            while True:
                conn, addr = ssock.accept()
                client_ip = addr[0]
                print(f"[+] Conexión segura desde {addr}")
                log_event(f"Intento de conexión desde {addr}")

                try:
                    credenciales = json.loads(conn.recv(1024).decode())
                except Exception as e:
                    log_event(f"Error leyendo credenciales de {addr}: {e}")
                    conn.close()
                    continue

                user_hash = USUARIOS_VALIDOS.get(credenciales.get('user'))
                if user_hash and user_hash == credenciales.get('hash'):
                    conn.send(b"AUTH_OK")
                    log_event(f"Autenticación exitosa para {credenciales.get('user')} desde {addr}")

                    while True:
                        data = conn.recv(1024).decode()
                        if not data or data == "exit":
                            log_event(f"Cliente {addr} desconectado")
                            break
                        respuesta = ejecutar_comando(data, addr)
                        conn.send(json.dumps(respuesta).encode())
                else:
                    conn.send(b"AUTH_FAIL")
                    log_event(f"Autenticación fallida desde {addr} con usuario {credenciales.get('use>
                    conn.close()

if __name__ == "__main__":
    iniciar_servidor()
