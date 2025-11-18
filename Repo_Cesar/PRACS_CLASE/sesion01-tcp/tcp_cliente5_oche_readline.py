import socket
import sys

ip = sys.argv[1] if len(sys.argv) > 1 else "localhost"
puerto = int(sys.argv[2]) if len(sys.argv) > 2 else 9999
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, puerto))

f = s.makefile(encoding="utf8", newline="\r\n")
mensajes = ["HOLA", "MUNDO", "TEST"]
for msg in mensajes:
    s.sendall((msg + "\r\n").encode("utf8"))
    resp = f.readline().strip()
    print(f"Enviado: {msg}, Recibido: {resp}")
f.close()
s.close()