import socket
import sys

# Acceso a argumentos: IP y puerto por defecto localhost:9999
if len(sys.argv) == 1:
    servidor = "localhost"
    puerto = 9999
elif len(sys.argv) == 3:
    servidor = sys.argv[1]
    puerto = int(sys.argv[2])
else:
    print("Uso: python udp_cliente1.py <mensaje> <puerto>")
    sys.exit(1)

# Crear socket UDP
cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while (mensaje := input("Escribe mensajes para enviar al servidor. 'FIN' para salir.")) != "FIN":
    cliente.sendto(mensaje.encode('utf-8'), (servidor, puerto))

#Esperar respuesta
respuesta, _ = cliente.recvfrom(1024)
print(f"Respuesta del servidor: {respuesta.decode('utf-8')}")

# Cerrar socket
cliente.close()