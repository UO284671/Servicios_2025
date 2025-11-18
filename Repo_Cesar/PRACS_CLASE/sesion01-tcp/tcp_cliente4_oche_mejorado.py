import socket
import sys

def recibe_mensaje(sock):
    buffer = []
    while True:
        byte = sock.recv(1)
        if not byte:
            return b"".join(buffer)
        buffer.append(byte)
        if len(buffer) >= 2 and buffer[-2:] == [b"\r", b"\n"]:
            return b"".join(buffer)

ip = sys.argv[1] if len(sys.argv) > 1 else "localhost"
puerto = int(sys.argv[2]) if len(sys.argv) > 2 else 9999
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, puerto))

mensajes = ["HOLA", "MUNDO", "TEST"]
for msg in mensajes:
    s.sendall((msg + "\r\n").encode("utf8"))
    resp = recibe_mensaje(s).decode("utf8")
    print(f"Enviado: {msg}, Recibido: {resp.strip()}")
s.close()
