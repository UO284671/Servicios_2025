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
        longitud = recibe_longitud(sd)
        if not longitud:
            print("Conexión cerrada por el cliente")
            sd.close()
            break
        longitud = int(longitud.decode("ascii").strip())
        mensaje = recvall(sd, longitud).decode("utf8")
        respuesta = mensaje[::-1]
        longitud_resp = f"{len(respuesta.encode('utf8'))}\n"
        sd.sendall((longitud_resp + respuesta).encode("utf8"))
s.close()
