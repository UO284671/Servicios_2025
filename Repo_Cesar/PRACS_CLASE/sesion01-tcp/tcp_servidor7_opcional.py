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
        longitud_bytes = recvall(sd, 2)
        if not longitud_bytes:
            print("Conexión cerrada por el cliente")
            sd.close()
            break
        longitud = struct.unpack(">H", longitud_bytes)[0]
        mensaje = recvall(sd, longitud).decode("utf8")
        respuesta = mensaje[::-1]
        longitud_resp = struct.pack(">H", len(respuesta.encode("utf8")))
        sd.sendall(longitud_resp + respuesta.encode("utf8"))
s.close()