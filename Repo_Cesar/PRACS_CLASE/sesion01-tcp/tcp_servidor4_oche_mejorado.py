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

puerto = int(sys.argv[1]) if len(sys.argv) > 1 else 9999
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", puerto))
s.listen(5)
print(f"Servidor oche escuchando en puerto {puerto}...")

while True:
    print("Esperando un cliente")
    sd, origen = s.accept()
    print(f"Nuevo cliente conectado desde {origen}")
    while True:
        mensaje = recibe_mensaje(sd)
        if not mensaje:
            print("Conexión cerrada por el cliente")
            sd.close()
            break
        mensaje = mensaje.decode("utf8")
        linea = mensaje[:-2]
        respuesta = linea[::-1]
        sd.sendall((respuesta + "\r\n").encode("utf8"))
s.close()