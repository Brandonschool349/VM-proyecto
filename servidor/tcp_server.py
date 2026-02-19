import socket
import psutil
import subprocess
import json

HOST = "0.0.0.0"
PORT = 5000

# 🔥 guardamos procesos lanzados
procesos = {}

def handle_command(cmd):

    # ---------- MONITOR ----------
    if cmd == "monitor":
        return {
            "cpu": psutil.cpu_percent(interval=1),
            "ram": psutil.virtual_memory().percent,
            "procesos_activos": len(procesos)
        }

    # ---------- LIST ----------
    elif cmd == "list":
        salida = []
        for pid, proc in procesos.items():
            if proc.poll() is None:  # sigue vivo
                salida.append({
                    "pid": pid,
                    "cmd": " ".join(proc.args)
                })
        return salida

    # ---------- RUN ----------
    elif cmd.startswith("run "):
        program = cmd[4:]
        try:
            proc = subprocess.Popen(program.split())
            procesos[proc.pid] = proc
            return {
                "status": f"Ejecutado {program}",
                "pid": proc.pid
            }
        except Exception as e:
            return {"error": str(e)}

    # ---------- STOP ----------
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

    else:
        return {"error": "Comando desconocido"}


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Servidor escuchando en puerto {PORT}")

    while True:
        conn, addr = s.accept()
        with conn:
            try:
                data = conn.recv(1024).decode().strip()
                response = handle_command(data)
                conn.send(json.dumps(response).encode())
            except Exception as e:
                conn.send(json.dumps({"error": str(e)}).encode())
