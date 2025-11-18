# tcp_cliente5_oche_readline.py
import socket
import sys

IP = sys.argv[1]
PUERTO = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PUERTO))

# Convertimos el socket en un fichero para leer respuestas
f = s.makefile(encoding="utf-8", newline="\r\n")

# 1. Enviamos TRES mensajes seguidos
print("Enviando 'UNO'...")
s.sendall(b"UNO\r\n")
print("Enviando 'DOS'...")
s.sendall(b"DOS\r\n")
print("Enviando 'TRES'...")
s.sendall(b"TRES\r\n")

# 2. Leemos TRES respuestas usando la función robusta y eficiente
print("--- Esperando respuestas ---")
try:
    # Usamos readline() para cada respuesta
    respuesta1 = f.readline()
    print("Respuesta 1:", repr(respuesta1))

    respuesta2 = f.readline()
    print("Respuesta 2:", repr(respuesta2))

    respuesta3 = f.readline()
    print("Respuesta 3:", repr(respuesta3))
    
except EOFError:
    print("Error: El servidor cerró la conexión inesperadamente.")

f.close() # Cerramos el "fichero"
s.close() # Cerramos el socket
print("Conexión cerrada.")