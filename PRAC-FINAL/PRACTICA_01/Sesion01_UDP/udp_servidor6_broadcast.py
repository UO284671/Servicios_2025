# udp_servidor6.py
import socket
import sys

# Puerto fijo indicado en el guion
PUERTO = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# IMPORTANTE: Activamos la opción de Broadcast
# SOL_SOCKET = Nivel del socket
# SO_BROADCAST = Opción a modificar
# 1 = Activar
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Enlazamos al puerto.
s.bind(('', PUERTO))

print(f"Servidor Broadcast escuchando en puerto {PUERTO}...")

while True:
    datos, origen = s.recvfrom(1024)
    mensaje = datos.decode('utf-8')
    
    # Lógica de respuestas según el protocolo "HOLA"
    if mensaje == "BUSCANDO HOLA":
        print(f"-> Recibida búsqueda de {origen}. Respondiendo disponibilidad.")
        s.sendto(b"IMPLEMENTO HOLA", origen)
        
    elif mensaje == "HOLA":
        print(f"-> Recibido saludo directo de {origen}.")
        # Respondemos con la IP del cliente (que está en la tupla origen[0])
        respuesta = f"HOLA: {origen[0]}"
        s.sendto(respuesta.encode('utf-8'), origen)