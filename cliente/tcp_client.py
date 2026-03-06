import socket, ssl, json, psutil, subprocess, hashlib, datetime, os

HOST = '192.168.10.10' 
PORT = 5000

USUARIOS_VALIDOS = {"admin": hashlib.sha256("admin123".encode()).hexdigest()}
procesos = {}

# CORRECCIÓN: Carpeta local para evitar PermissionError
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "server_audit.log")

def log_event(event):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f: f.write(f"[{timestamp}] {event}\n")

def list_logs():
    try:
        with open(LOG_FILE, "r") as f: return f.readlines()[-50:]
    except Exception as e: return [f"Error leyendo logs: {e}"]

def ejecutar_comando(cmd, client_addr):
    log_event(f"Comando recibido de {client_addr}: {cmd}")
    if cmd == "monitor":
        return {"cpu": psutil.cpu_percent(interval=1), "ram": psutil.virtual_memory().percent, "procesos_activos": len(procesos)}
    elif cmd == "list":
        salida = []
        for pid, proc in list(procesos.items()):
            if proc.poll() is None: salida.append({"pid": pid, "cmd": " ".join(proc.args)})
            else: del procesos[pid]
        return salida
    elif cmd.startswith("run "):
        program = cmd[4:]
        try:
            proc = subprocess.Popen(program.split())
            procesos[proc.pid] = proc
            return {"status": f"Ejecutado {program}", "pid": proc.pid}
        except Exception as e: return {"error": str(e)}
    elif cmd.startswith("stop "):
        try:
            pid = int(cmd[5:])
            if pid in procesos:
                procesos[pid].terminate()
                del procesos[pid]
                return {"status": f"Proceso {pid} terminado"}
            else: return {"error": "PID no encontrado"}
        except Exception as e: return {"error": str(e)}
    elif cmd == "list_logs": return list_logs()
    else: return {"error": "Comando desconocido"}

def iniciar_servidor():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen(5)
        print(f"[*] Servidor TLS escuchando en {HOST}:{PORT}")
        with context.wrap_socket(sock, server_side=True) as ssock:
            while True:
                conn, addr = ssock.accept()
                try:
                    credenciales = json.loads(conn.recv(1024).decode())
                    if USUARIOS_VALIDOS.get(credenciales.get('user')) == credenciales.get('hash'):
                        conn.send(b"AUTH_OK")
                        while True:
                            data = conn.recv(1024).decode()
                            if not data or data == "exit": break
                            conn.send(json.dumps(ejecutar_comando(data, addr)).encode())
                    else:
                        conn.send(b"AUTH_FAIL")
                        # CORRECCIÓN: La línea que estaba cortada ya está bien
                        log_event(f"Autenticación fallida de {credenciales.get('user')}")
                except Exception as e: log_event(f"Error: {e}")
                finally: conn.close()

if __name__ == "__main__": iniciar_servidor()