import socket
import sys

def recvall(sock, n):
    datos = b""
    while len(datos) < n:
        paquete = sock.recv(n - len(datos))
        if not paquete:
            return datos
        datos += paquete
    return datos

def recibe_longitud(sock):
    buffer = []
    while True:
        byte = sock.recv(1)
        if not byte:
            return b"".join(buffer)
        buffer.append(byte)
        if byte == b"\n":
            return b"".join(buffer)

ip = sys.argv[1] if len(sys.argv) > 1 else "localhost"
puerto = int(sys.argv[2]) if len(sys.argv) > 2 else 9999
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, puerto))

mensajes = ["HOLA", "MUNDO", "TEST"]
for msg in mensajes:
    longitud = f"{len(msg.encode('utf8'))}\n"
    s.sendall((longitud + msg).encode("utf8"))
    longitud_resp = recibe_longitud(s).decode("ascii").strip()
    resp = recvall(s, int(longitud_resp)).decode("utf8")
    print(f"Enviado: {msg}, Recibido: {resp}")
s.close()