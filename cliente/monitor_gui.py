import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import json, ssl, socket, hashlib, threading

HOST = '192.168.10.20'  # IP del Middleware variable para facilitar cambios futuros
PORT = 6000
USER = "admin"
PASSWORD = "admin123"
HASH = hashlib.sha256(PASSWORD.encode()).hexdigest()

def enviar_comando(comando, callback):
    def tarea():
        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

            with socket.create_connection((HOST, PORT)) as sock:
                with context.wrap_socket(sock, server_hostname=HOST) as ssock:
                    ssock.send(json.dumps({"user": USER, "hash": HASH}).encode())
                    if ssock.recv(1024).decode() != "AUTH_OK":
                        root.after(0, lambda: messagebox.showerror("Error", "Auth fallida"))
                        return
                        
                    ssock.send(comando.encode())
                    data = ssock.recv(4096).decode()
                    root.after(0, lambda: callback(json.loads(data)))
        except Exception as e:
            root.after(0, lambda: messagebox.showerror("Error", str(e)))
    threading.Thread(target=tarea, daemon=True).start()

def actualizar_monitor():
    def cb(res):
        if res and "cpu" in res:
            cpu_label.config(text=f"CPU: {res['cpu']}%")
            ram_label.config(text=f"RAM: {res['ram']}%")
            procesos_text.delete(1.0, tk.END)
            procesos_text.insert(tk.END, f"Procesos activos (GUI): {res.get('procesos_activos', 0)}\n")
    enviar_comando("monitor", cb)

def listar_procesos():
    def cb(res):
        if res is not None:
            procesos_text.delete(1.0, tk.END)
            if not res: procesos_text.insert(tk.END, "Sin procesos.\n")
            for p in res: procesos_text.insert(tk.END, f"PID: {p['pid']} | CMD: {p['cmd']}\n")
    enviar_comando("list", cb)

def detener_proceso():
    pid = simpledialog.askinteger("Stop", "Ingrese PID:")
    if pid:
        enviar_comando(f"stop {pid}", lambda res: [messagebox.showinfo("OK", str(res)), listar_procesos()])

def ejecutar_proceso():
    cmd = simpledialog.askstring("Run", "Comando (ej. sleep 500):")
    if cmd:
        enviar_comando(f"run {cmd}", lambda res: [messagebox.showinfo("OK", str(res)), listar_procesos()])

def mostrar_logs():
    def cb(res):
        if res:
            logs_text.delete(1.0, tk.END)
            for l in res: logs_text.insert(tk.END, f"{l.strip()}\n")
    enviar_comando("list_logs", cb)

root = tk.Tk()
root.title("Monitor Distribuido (TLS)")
root.geometry("600x600")

frame_monitor = tk.LabelFrame(root, text="Recursos", padx=10, pady=10)
frame_monitor.pack(fill="x", padx=10, pady=5)
cpu_label = tk.Label(frame_monitor, text="CPU: 0%", font=("Arial", 12, "bold")); cpu_label.pack(anchor="w")
ram_label = tk.Label(frame_monitor, text="RAM: 0%", font=("Arial", 12, "bold")); ram_label.pack(anchor="w")
tk.Button(frame_monitor, text="Monitor", command=actualizar_monitor).pack()

frame_proc = tk.LabelFrame(root, text="Procesos", padx=10, pady=10)
frame_proc.pack(fill="both", expand=True, padx=10, pady=5)
procesos_text = scrolledtext.ScrolledText(frame_proc, height=8); procesos_text.pack(fill="both", expand=True)
btn_frame = tk.Frame(frame_proc); btn_frame.pack()
tk.Button(btn_frame, text="Listar", command=listar_procesos).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Ejecutar", command=ejecutar_proceso).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Detener", command=detener_proceso).grid(row=0, column=2, padx=5)

frame_logs = tk.LabelFrame(root, text="Logs", padx=10, pady=10)
frame_logs.pack(fill="both", expand=True, padx=10, pady=5)
logs_text = scrolledtext.ScrolledText(frame_logs, height=8, bg="black", fg="lightgreen"); logs_text.pack(fill="both", expand=True)
tk.Button(frame_logs, text="Logs", command=mostrar_logs).pack()

root.mainloop()