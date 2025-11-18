import socket
import sys

ip = sys.argv[1] if len(sys.argv) > 1 else "localhost"
puerto = int(sys.argv[2]) if len(sys.argv) > 2 else 9999
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, puerto))

mensajes = ["HOLA", "MUNDO", "TEST"]
for msg in mensajes:
    s.sendall((msg + "\r\n").encode("utf8"))
    resp = s.recv(80).decode("utf8")
    print(f"Enviado: {msg}, Recibido: {resp.strip()}")
s.close()