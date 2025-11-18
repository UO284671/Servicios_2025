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
    while True:
        mensaje = sd.recv(80)  # Máx 80 bytes
        if not mensaje:  # Cliente cerró
            print("Conexión cerrada por el cliente")
            sd.close()
            break
        mensaje = mensaje.decode("utf8")
        linea = mensaje[:-2]  # Quitar \r\n
        respuesta = linea[::-1]  # Invertir
        sd.sendall((respuesta + "\r\n").encode("utf8"))
s.close()