import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import json, ssl, socket, hashlib
from datetime import datetime

HOST = '192.168.10.20'  # IP del servidor SrvA
PORT = 6000

USER = "admin"
PASSWORD = "admin123"
HASH = hashlib.sha256(PASSWORD.encode()).hexdigest()

# Funci  n para enviar comandos al servidor
def enviar_comando(comando):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((HOST, PORT)) as sock:
            with context.wrap_socket(sock, server_hostname=HOST) as ssock:
                creds = json.dumps({"user": USER, "hash": HASH})
                ssock.send(creds.encode())
                auth_resp = ssock.recv(1024).decode()
                if auth_resp != "AUTH_OK":
                    messagebox.showerror("Error", "Autenticaci  n fallida")
                    return None
                ssock.send(comando.encode())
                data = ssock.recv(4096).decode()
                return json.loads(data)
    except Exception as e:
        messagebox.showerror("Error de conexi  n", str(e))
        return None

# Funciones de la interfaz
def actualizar_monitor():
    res = enviar_comando("monitor")
    if res:
        cpu_label.config(text=f"CPU: {res['cpu']}%")
        ram_label.config(text=f"RAM: {res['ram']}%")
        procesos_text.delete(1.0, tk.END)
        procesos_text.insert(tk.END, f"Procesos activos: {res['procesos_activos']}\n")

def listar_procesos():
    res = enviar_comando("list")
    if res:
        procesos_text.delete(1.0, tk.END)
        for p in res:
            procesos_text.insert(tk.END, f"PID: {p['pid']} | CMD: {p['cmd']}\n")

def detener_proceso():
    pid = simpledialog.askinteger("Detener proceso", "Ingrese PID:")
    if pid:
        res = enviar_comando(f"stop {pid}")
        if res:
            messagebox.showinfo("Resultado", str(res))
            listar_procesos()

def ejecutar_proceso():
    cmd = simpledialog.askstring("Ejecutar proceso", "Ingrese comando:")
    if cmd:
        res = enviar_comando(f"run {cmd}")
        if res:
            messagebox.showinfo("Resultado", str(res))
            listar_procesos()

def mostrar_logs():
    res = enviar_comando("list_logs")
    if res:
        logs_text.delete(1.0, tk.END)
        for l in res:
            logs_text.insert(tk.END, f"{l}\n")

# Crear ventana principal
root = tk.Tk()
root.title("Monitor Distribuido")
root.geometry("600x600")
root.configure(bg="#f0f0f0")

# Secci  n Monitor
frame_monitor = tk.LabelFrame(root, text="Monitor de recursos", padx=10, pady=10)
frame_monitor.pack(padx=10, pady=5, fill="x")
cpu_label = tk.Label(frame_monitor, text="CPU: 0%", font=("Arial", 12))
cpu_label.pack(anchor="w")
ram_label = tk.Label(frame_monitor, text="RAM: 0%", font=("Arial", 12))
ram_label.pack(anchor="w")
tk.Button(frame_monitor, text="Actualizar Monitor", command=actualizar_monitor).pack(pady=5)

# Secci  n Procesos
frame_proc = tk.LabelFrame(root, text="Procesos activos", padx=10, pady=10)
frame_proc.pack(padx=10, pady=5, fill="both", expand=True)
procesos_text = scrolledtext.ScrolledText(frame_proc, height=10)
procesos_text.pack(fill="both", expand=True)
btn_frame = tk.Frame(frame_proc)
btn_frame.pack(pady=5)
tk.Button(btn_frame, text="Listar Procesos", command=listar_procesos).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Detener Proceso", command=detener_proceso).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Ejecutar Proceso", command=ejecutar_proceso).grid(row=0, column=2, padx=5)

# Secci  n Logs
frame_logs = tk.LabelFrame(root, text="Logs del servidor", padx=10, pady=10)
frame_logs.pack(padx=10, pady=5, fill="both", expand=True)
logs_text = scrolledtext.ScrolledText(frame_logs, height=10)
logs_text.pack(fill="both", expand=True)
tk.Button(frame_logs, text="Actualizar Logs", command=mostrar_logs).pack(pady=5)

root.mainloop()
