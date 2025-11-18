import socket
import sys

puerto = int(sys.argv[1]) if len(sys.argv) > 1 else 9999
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", puerto))
s.listen(5)
print(f"Servidor oche escuchando en puerto {puerto}...")

while True:
    print("Esperando un cliente")
    sd, origen = s.accept()
    print(f"Nuevo cliente conectado desde {origen}")
    f = sd.makefile(encoding="utf8", newline="\r\n")
    while True:
        mensaje = f.readline()
        if not mensaje:
            print("Conexión cerrada por el cliente")
            f.close()
            sd.close()
            break
        linea = mensaje[:-2]
        respuesta = linea[::-1]
        sd.sendall((respuesta + "\r\n").encode("utf8"))
    f.close()
s.close()
