import socket
import sys

# Puerto por defecto o desde argumentos
puerto = int(sys.argv[1]) if len(sys.argv) > 1 else 9999

# Crear socket TCP
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
        datos = sd.recv(5)  # Leer 5 bytes
        if not datos:  # Cliente cerró conexión
            print("Conexión cerrada por el cliente")
            sd.close()
            continuar = False
        else:
            datos = datos.decode("ascii")  # Asumimos ASCII
            if datos == "FINAL":
                print("Recibido mensaje de finalización")
                sd.close()
                continuar = False
            else:
                print(f"Recibido mensaje: {datos}")
s.close()