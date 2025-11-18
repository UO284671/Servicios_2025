import socket
import sys
import struct

def recvall(sock, n):
    datos = b""
    while len(datos) < n:
        paquete = sock.recv(n - len(datos))
        if not paquete:
            return datos
        datos += paquete
    return datos

ip = sys.argv[1] if len(sys.argv) > 1 else "localhost"
puerto = int(sys.argv[2]) if len(sys.argv) > 2 else 9999
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, puerto))

mensajes = ["HOLA", "MUNDO", "TEST"]
for msg in mensajes:
    msg_bytes = msg.encode("utf8")
    longitud = struct.pack(">H", len(msg_bytes))
    s.sendall(longitud + msg_bytes)
    longitud_resp = recvall(s, 2)
    longitud = struct.unpack(">H", longitud_resp)[0]
    resp = recvall(s, longitud).decode("utf8")
    print(f"Enviado: {msg}, Recibido: {resp}")
s.close()