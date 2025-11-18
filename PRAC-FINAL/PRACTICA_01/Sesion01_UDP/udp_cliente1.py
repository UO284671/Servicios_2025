# udp_cliente1.py
import socket
import sys

# 1. Obtenemos la IP y Puerto del servidor de los argumentos
if len(sys.argv) == 3:
    IP_SERVIDOR = sys.argv[1]
    PUERTO_SERVIDOR = int(sys.argv[2])
elif len(sys.argv) == 2:
    IP_SERVIDOR = sys.argv[1]
    PUERTO_SERVIDOR = 9999
else:
    IP_SERVIDOR = 'localhost'
    PUERTO_SERVIDOR = 9999

# 2. Logica del cliente UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor = (IP_SERVIDOR, PUERTO_SERVIDOR)

# 3. Bucle principal para enviar mensajes
print(f"Enviando mensajes a {IP_SERVIDOR}:{PUERTO_SERVIDOR}")
print("Escribe 'FIN' para terminar.")

while True:
    mensaje = input("Mensaje: ")
    
    if mensaje == "FIN":
        break
    
    s.sendto(mensaje.encode('utf-8'), (IP_SERVIDOR, PUERTO_SERVIDOR))

# 4. Cerramos el socket al terminar
s.close()
print("Cliente finalizado.")