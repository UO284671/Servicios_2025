# tcp_cliente3_oche_envia_seguido.py
import socket
import sys

IP = sys.argv[1]
PUERTO = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PUERTO))

# 1. Enviamos TRES mensajes seguidos
print("Enviando 'UNO'...")
s.sendall(b"UNO\r\n")
print("Enviando 'DOS'...")
s.sendall(b"DOS\r\n")
print("Enviando 'TRES'...")
s.sendall(b"TRES\r\n")

# 2. Leemos TRES respuestas (o lo intentamos)
print("--- Esperando respuestas ---")
try:
    respuesta1 = s.recv(80)
    print("Respuesta 1:", repr(respuesta1)) # Usamos repr()

    respuesta2 = s.recv(80)
    print("Respuesta 2:", repr(respuesta2))

    respuesta3 = s.recv(80)
    print("Respuesta 3:", repr(respuesta3))
    
except socket.timeout:
    print("Error: Timeout esperando respuesta.")

s.close()
print("Conexión cerrada.")