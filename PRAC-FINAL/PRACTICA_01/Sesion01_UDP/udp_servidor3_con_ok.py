# udp_servidor3.py
import socket
import sys
import random

# 1. Obtenemos el puerto de los argumentos (9999 por defecto)
if len(sys.argv) > 1:
    PUERTO = int(sys.argv[1])
else:
    PUERTO = 9999

print(f"Servidor3 UDP iniciando en el puerto {PUERTO}")

# 2. Inicia la lógica del servidor3 UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 3. Enlazamos el socket al puerto
s.bind(('', PUERTO))

# 4. Bucle principal para esperar datagramas
print("Servidor3 UDP (simula perdidas) esperando mensajes...")
while True:
    datos, direccion_origen = s.recvfrom(1024)

    # Simulación de pérdida (50% de probabilidad)
    if random.randint(0,1) == 0:                    # 0 = Perdido
        print(f"Simulando paquete perdido...")
    else:
        mensaje = datos.decode('utf-8')
        print(f"Recibido de {direccion_origen}: {mensaje}")

        # Enviamos el "OK" de vuelta al remitente
        s.sendto(b"OK", direccion_origen)

s.close()