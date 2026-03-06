🛡️ Sistema Distribuido Seguro (TLS/SSL) para Administración de Sistemas Operativos

Este proyecto implementa un sistema distribuido seguro diseñado para la administración remota de sistemas operativos Linux mediante una arquitectura de tres nodos independientes: Cliente, Middleware/Proxy y Servidor Gestor.

El sistema elimina las comunicaciones en texto plano y utiliza cifrado TLS 1.3, autenticación de usuarios basada en hash SHA-256, y un sistema de monitoreo de recursos en tiempo real.

El objetivo es demostrar conceptos clave de sistemas operativos distribuidos, seguridad en redes y administración remota de procesos.

Proyecto desarrollado para la materia de Sistemas Operativos.

🏗️ Arquitectura del Sistema

El sistema se compone de tres componentes principales desplegados en máquinas virtuales independientes, simulando un entorno de infraestructura distribuida.

Servidor Gestor (SrvA)

El servidor gestor es el nodo encargado de interactuar directamente con el sistema operativo.

Funciones principales:

Ejecutar comandos del sistema

Obtener información del kernel

Administrar procesos

Generar respuestas en formato JSON

El servidor utiliza la librería psutil para acceder a métricas del sistema como:

uso de CPU

uso de memoria

lista de procesos activos

Todas las comunicaciones entrantes se realizan mediante TLS cifrado.

Middleware / Proxy Seguro (SrvB)

El middleware actúa como una capa intermedia de seguridad y distribución de tráfico.

Funciones principales:

Recibir solicitudes del cliente

Validar la comunicación segura

Reenviar peticiones al servidor gestor

Retornar la respuesta al cliente

Este componente permite:

desacoplar el cliente del servidor

mejorar la seguridad

facilitar la escalabilidad

controlar el flujo de comunicaciones

El middleware también permite simular arquitecturas utilizadas en infraestructura cloud y microservicios.

Cliente

El cliente es la interfaz que permite al usuario interactuar con el sistema distribuido.

Funciones principales:

autenticación de usuarios

envío de comandos remotos

recepción de resultados

formateo de respuestas del servidor

La contraseña del usuario no se envía en texto plano.
Antes de transmitirse, se aplica un hash SHA-256 para proteger las credenciales.

🔐 Seguridad Implementada

El sistema incluye múltiples capas de seguridad.

Cifrado de Comunicación

Se implementa TLS/SSL utilizando OpenSSL y la librería ssl de Python, garantizando:

confidencialidad de los datos

integridad de la comunicación

protección contra ataques de sniffing

Las conexiones cliente-servidor utilizan certificados X.509.

Autenticación de Usuarios

El sistema implementa autenticación mediante:

verificación de usuario

comparación de contraseñas con hash SHA-256

Esto evita almacenar o transmitir contraseñas en texto plano.

Protección del Entorno

El sistema fue desplegado en máquinas virtuales Linux, utilizando herramientas comunes de seguridad en entornos Red Hat/Linux como:

control de usuarios del sistema

reglas de red

firewall del sistema (Firewalld)

Esto simula prácticas utilizadas en entornos reales de infraestructura cloud.

🖥️ Entorno de Despliegue

El sistema fue probado en máquinas virtuales Linux para simular un entorno distribuido.

Configuración utilizada:

3 máquinas virtuales

sistema operativo Linux

comunicación mediante red interna

Esta arquitectura permite simular el despliegue de aplicaciones en infraestructuras cloud o centros de datos distribuidos.

⚙️ Requisitos Previos

Para ejecutar el sistema se requiere instalar las siguientes dependencias.

Dependencias del Sistema

Instalar Python y OpenSSL:

sudo apt update
sudo apt install python3 python3-pip openssl -y
Librerías de Python

El sistema utiliza librerías para monitoreo y visualización de datos:

pip3 install psutil matplotlib

En algunas distribuciones Linux también se puede instalar con:

sudo apt install python3-psutil python3-matplotlib
🔑 Generación de Certificados TLS

Para habilitar la comunicación segura es necesario generar certificados X.509.

Ejecutar el siguiente comando dentro del directorio del proyecto:

openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

Esto generará:

key.pem → clave privada

cert.pem → certificado público

Durante el proceso se solicitarán datos como país u organización.
Se pueden dejar los valores por defecto.

⚠️ Importante:

Los archivos cert.pem y key.pem no deben subirse a repositorios públicos.

Se recomienda agregarlos al archivo:

.gitignore
🚀 Instrucciones de Ejecución

El sistema debe iniciarse en el siguiente orden.

Se recomienda usar tres terminales distintas o tres máquinas virtuales.

1. Iniciar el Servidor Gestor
python3 tcp_server.py

Mensaje esperado:

Servidor escuchando de forma SEGURA...
2. Iniciar el Middleware
python3 middleware.py

Mensaje esperado:

Middleware seguro escuchando conexiones...
3. Iniciar el Cliente
python3 cliente.py

El sistema solicitará autenticación.

Credenciales de ejemplo:

Usuario:

admin

Contraseña:

admin123
📊 Comandos Soportados

Una vez autenticado, el usuario puede ejecutar comandos remotos.

list

Obtiene la lista de procesos activos en el sistema.

Salida:

PID

nombre del proceso

monitor

Muestra métricas del sistema en tiempo real.

Incluye:

uso de CPU

uso de memoria RAM

exit

Cierra la conexión segura con el servidor.

🖥️ Interfaz Gráfica (GUI)

El sistema incluye una interfaz gráfica desarrollada con Tkinter para facilitar la administración del sistema distribuido.

Funciones principales de la interfaz:

visualizar procesos activos

iniciar procesos remotos

detener procesos

monitorear CPU y RAM

visualizar registros del sistema

La interfaz se comunica con el middleware utilizando el mismo protocolo TCP utilizado por el cliente de consola.

Debido a limitaciones del entorno gráfico de las máquinas virtuales, la validación visual completa de la interfaz se encuentra en proceso. Sin embargo, la lógica de comunicación y los comandos remotos han sido probados correctamente.

🧪 Pruebas Realizadas

Se realizaron diferentes tipos de pruebas para validar el funcionamiento del sistema.

Tipo de prueba	Resultado
Conexión TLS	Exitosa
Autenticación de usuarios	Exitosa
Ejecución de comandos remotos	Exitosa
Monitoreo de CPU y RAM	Correcto
Comunicación cliente-servidor	Estable

Estas pruebas confirman que el sistema funciona correctamente dentro de un entorno distribuido seguro.

📈 Mejoras y Optimización

Durante el desarrollo se realizaron mejoras para optimizar el sistema:

uso de psutil para monitoreo eficiente del sistema

uso de JSON para estructurar respuestas del servidor

separación de responsabilidades entre nodos

uso de middleware para mejorar la escalabilidad

📚 Tecnologías Utilizadas

Python 3

OpenSSL

TLS / SSL

psutil

matplotlib

Tkinter

Linux / Ubuntu Server

Máquinas Virtuales

👨‍💻 Autor

Proyecto desarrollado para la materia de Sistemas Operativos.

Implementa conceptos de:

sistemas distribuidos

seguridad en redes

administración de procesos

virtualización

monitoreo de recursos del sistema
