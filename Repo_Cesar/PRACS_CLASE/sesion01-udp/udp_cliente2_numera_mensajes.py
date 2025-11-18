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

contador = 1
print("Escribe mensajes. 'FIN' para salir.")
while True:
    linea = input("> ")
    if linea == "FIN":
        break
    # Numerar: "1: mensaje"
    mensaje = f"{contador}: {linea}"
    cliente.sendto(mensaje.encode("utf-8"), (servidor, puerto))
    contador += 1

cliente.close()