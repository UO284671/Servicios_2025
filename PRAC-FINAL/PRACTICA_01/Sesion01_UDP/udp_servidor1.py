# udp_servidor1.py
import socket
import sys

# 1. Obtenemos el puerto de los argumentos (9999 por defecto)
if len(sys.argv) > 1:
    PUERTO = int(sys.argv[1])
else:
    PUERTO = 9999

print(f"Servidor UDP iniciando en el puerto {PUERTO}")

# 2. Inicia la lógica del servidor UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 3. Enlazamos el socket al puerto
try:
    s.bind(('', PUERTO))
except socket.error:
    print(f"Error al enlazar el socket al puerto")
    exit(1)

# 4. Bucle principal para esperar datagramas
print("Servidor UDP esperando mensajes...")
while True:
    datos, direccion_origen = s.recvfrom(1024)  # 1024 es el tamaño del buffer
    mensaje = datos.decode('utf-8')
    print(f"Recibido de {direccion_origen}: {mensaje}")

s.close()


