import socket
import sys

# IP y puerto por defecto o desde argumentos
ip = sys.argv[1] if len(sys.argv) > 1 else "localhost"
puerto = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

# Crear socket TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, puerto))

# Enviar 5 veces "ABCDE"
for _ in range(5):
    s.send("ABCDE".encode("ascii"))  # 5 bytes

# Enviar "FINAL"
s.send("FINAL".encode("ascii"))
s.close()