# 🛡️ Sistema Distribuido Seguro (TLS/SSL) - Administración de SO

Este proyecto implementa una arquitectura distribuida de tres nodos (Cliente, Middleware/Proxy y Servidor Gestor) diseñada para la administración remota y segura de sistemas operativos basados en Linux. 

El sistema abandona las conexiones vulnerables en texto plano, implementando túneles criptográficos (TLS 1.3), autenticación basada en Hash (SHA-256) y monitoreo de recursos de hardware en tiempo real.

## 🏗️ Arquitectura del Proyecto

1. **Servidor Gestor (SrvA):** Ejecuta comandos a nivel del sistema operativo (listar procesos, monitorear CPU/RAM) y retorna los resultados en formato JSON.
2. **Middleware (SrvB):** Actúa como un túnel blindado. Recibe las peticiones del cliente y las reenvía al servidor de forma segura, distribuyendo la carga de red.
3. **Cliente:** Interfaz interactiva que solicita credenciales, cifra la contraseña antes de enviarla y formatea la respuesta del servidor.

---

## ⚙️ Requisitos Previos

Para ejecutar este proyecto en un entorno virtualizado (ej. Ubuntu Server), necesitas instalar las siguientes dependencias:

### 1. Dependencias del Sistema (Linux)
Asegúrate de tener instalado Python 3 y OpenSSL:

---------------------------
sudo apt update
sudo apt install python3 python3-pip openssl -y
---------------------------

2. Librerías de Python
El proyecto requiere módulos específicos para el monitoreo del sistema operativo y la generación de reportes visuales:

-------------------------------
pip3 install psutil matplotlib
-------------------------------

(Nota: En versiones recientes de Ubuntu, puede que necesites usar el flag --user o instalar vía sudo apt install python3-psutil python3-matplotlib).

Generación de Llaves y Certificados (IMPORTANTE)
El sistema utiliza cifrado asimétrico para asegurar la comunicación. El código no funcionará si no generas los certificados X.509 en el directorio de ejecución.

Ejecuta el siguiente comando en la terminal (dentro de la carpeta donde están tus scripts de Python) para generar una llave privada RSA de 4096 bits y un certificado autofirmado válido por 365 días:

---------------------------------
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
Durante la generación, el sistema te pedirá algunos datos (País, Estado, Organización). Puedes presionar Enter para dejar los valores por defecto.
---------------------------------

⚠️ Advertencia de Seguridad: Los archivos cert.pem y key.pem generados NO deben ser subidos a repositorios públicos. Asegúrate de incluirlos en tu archivo .gitignore.

🚀 Instrucciones de Ejecución
El orden de ejecución de los nodos es estricto para evitar errores de conexión (ConnectionRefusedError). Se deben abrir tres terminales distintas (o ejecutar en máquinas separadas cambiando las variables HOST en el código):

1. Iniciar el Servidor Gestor:

-------------------------
python3 tcp_server.py
(Deberá mostrar: "Servidor escuchando de forma SEGURA...")
-------------------------

2. Iniciar el Middleware / Proxy:

------------------------
python3 middleware.py
(Deberá mostrar: "Middleware BLINDADO escuchando...")
------------------------


3. Iniciar el Cliente:

-------------------
python3 cliente.py
-------------------
Al iniciar el cliente, el sistema solicitará autenticación. Utiliza las credenciales configuradas en la base de datos simulada del servidor (ej. Usuario: admin, Password: admin123).

📊 Comandos Soportados
Una vez autenticado, el cliente soporta los siguientes comandos remotos:
---------------------------------------------
list: Retorna un objeto JSON con el PID y Nombre de los procesos activos en el núcleo del sistema (ej. systemd).

monitor: Retorna el porcentaje exacto de consumo de CPU y Memoria RAM en tiempo real.

exit: Cierra el túnel de forma segura.
---------------------------------------

Desarrollado para la materia de Sistemas Operativos.