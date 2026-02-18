import socket
import json

MIDDLEWARE_HOST = '192.168.50.11'
MIDDLEWARE_PORT = 6000

while True:
    cmd = input("Comando (monitor, list, run <prog>, stop <PID>, servers, salir): ").strip()
    if cmd.lower() == "salir":
        break

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((MIDDLEWARE_HOST, MIDDLEWARE_PORT))
            s.send(cmd.encode())
            data = s.recv(4096)

        # Intentamos decodificar JSON
        try:
            resultado = json.loads(data.decode())
        except:
            resultado = {"error": "Respuesta inválida"}

        print(json.dumps(resultado, indent=4))

    except Exception as e:
        print("Error de conexión:", e)