import socket
import sys

# ... (mismo código de IP/puerto, connect que Ej1)
ip = sys.argv[1] if len(sys.argv) > 1 else "localhost"
puerto = int(sys.argv[2]) if len(sys.argv) > 2 else 9999
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, puerto))

# Enviar con sendall
for _ in range(5):
    s.sendall("ABCDE".encode("ascii"))
s.sendall("FINAL".encode("ascii"))
s.close()