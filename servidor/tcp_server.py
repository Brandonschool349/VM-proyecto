import socket
import psutil
import subprocess
import json

HOST = "0.0.0.0"
PORT = 5000

def handle_command(cmd):
    if cmd == "monitor":
        return {
            "cpu": psutil.cpu_percent(interval=1),
            "ram": psutil.virtual_memory().percent
        }

    elif cmd == "list":
        procs = []
        for p in psutil.process_iter(['pid','name']):
            procs.append(p.info)
        return procs[:10]  # limitamos salida

    elif cmd.startswith("run "):
        program = cmd[4:]
        try:
            subprocess.Popen(program.split())
            return {"status": f"Ejecutado {program}"}
        except Exception as e:
            return {"error": str(e)}

    elif cmd.startswith("stop "):
        try:
            pid = int(cmd[5:])
            p = psutil.Process(pid)
            p.terminate()
            return {"status": f"Proceso {pid} terminado"}
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
                data = conn.recv(1024).decode()
                response = handle_command(data)
                conn.send(json.dumps(response).encode())
            except Exception as e:
                conn.send(json.dumps({"error": str(e)}).encode())