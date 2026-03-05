import matplotlib.pyplot as plt
import psutil
import time

muestras = []
cpu_log = []
ram_log = []

print("Recolectando métricas de rendimiento (SrvA)...")

for i in range(1, 6):
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    muestras.append(i)
    cpu_log.append(cpu)
    ram_log.append(ram)
    print(f"Muestra {i}: CPU {cpu}% | RAM {ram}%")

plt.figure(figsize=(8, 5))
plt.plot(muestras, cpu_log, label='Uso de CPU (%)', marker='o', color='tab:red', linewidth=2)
plt.plot(muestras, ram_log, label='Uso de RAM (%)', marker='s', color='tab:blue', linewidth=2)

plt.title('Análisis de Rendimiento - Sistema Distribuido')
plt.xlabel('Número de Muestra')
plt.ylabel('Porcentaje de Uso (%)')
plt.legend()
plt.grid(True, linestyle='--')

plt.savefig('grafica_final.png')
print("\n[+] Gráfica generada exitosamente como 'grafica_final.png'")