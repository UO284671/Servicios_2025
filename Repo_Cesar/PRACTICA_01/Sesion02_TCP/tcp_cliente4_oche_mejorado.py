# tcp_cliente4_oche_mejorado.py
import socket
import sys

# --- Función del Ejercicio 4 (Técnica eficiente byte-a-byte) ---
def recibe_mensaje(sd):
    """
    Lee byte a byte del socket (sd) hasta encontrar el delimitador \r\n.
    Usa la técnica eficiente de lista + join.
    """
    buffer_lista = []
    while True:
        byte = sd.recv(1)
        if not byte:
            raise EOFError("Socket cerrado por el servidor")
        
        buffer_lista.append(byte)
        
        if byte == b"\n":
            return b"".join(buffer_lista)
# --- Fin de la función ---

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

# 2. Leemos TRES respuestas usando la función robusta
print("--- Esperando respuestas ---")
try:
    # Usamos la nueva función para cada respuesta
    respuesta1 = recibe_mensaje(s)
    print("Respuesta 1:", repr(respuesta1)) # Usamos repr()

    respuesta2 = recibe_mensaje(s)
    print("Respuesta 2:", repr(respuesta2))

    respuesta3 = recibe_mensaje(s)
    print("Respuesta 3:", repr(respuesta3))
    
except EOFError:
    print("Error: El servidor cerró la conexión inesperadamente.")

s.close()
print("Conexión cerrada.")