import socket
import sys

def recvall(sock, n):
    datos = b""
    while len(datos) < n:
        paquete = sock.recv(n - len(datos))
        if not paquete:  # Cliente cerró conexión
            return datos
        datos += paquete
    return datos

# ... (mismo código de puerto, bind, listen que Ej1)
puerto = int(sys.argv[1]) if len(sys.argv) > 1 else 9999
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", puerto))
s.listen(5)
print(f"Servidor escuchando en puerto {puerto}...")

while True:
    print("Esperando un cliente")
    sd, origen = s.accept()
    print(f"Nuevo cliente conectado desde {origen}")
    continuar = True
    while continuar:
        datos = recvall(sd, 5)  # Usar recvall
        if not datos:
            print("Conexión cerrada por el cliente")
            sd.close()
            continuar = False
        else:
            datos = datos.decode("ascii")
            if datos == "FINAL":
                print("Recibido mensaje de finalización")
                sd.close()
                continuar = False
            else:
                print(f"Recibido mensaje: {datos}")
s.close()