import socket
import sys

# Acceso a argumentos: puerto por defecto 9999
if len(sys.argv) > 2:
    print("Uso: python udp_servidor1.py <puerto>")
    sys.exit(1)
elif len(sys.argv) == 1:
    puerto = 9999
else:
    puerto = int(sys.argv[1])
    

# Crear socket UDP
servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind al puerto ("" significa cualquier IP)
servidor.bind(('localhost', puerto))
print(f"Servidor escuchando en puerto {puerto}...")


while True:
    datagrama, origen = servidor.recvfrom(1024)
    mensaje = datagrama.decode("utf-8")
    print(f"Datagrama recibido de {origen}: {mensaje}")
    # Enviar "OK"
    servidor.sendto("OK".encode("utf-8"), origen)