# tcp_servidor1.py
import socket
import sys
import time

# Puerto (o 9999 por defecto)
PUERTO = int(sys.argv[1]) if len(sys.argv) > 1 else 9999

# Creación del socket de escucha
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Asignarle puerto
s.bind(("", PUERTO))

# Ponerlo en modo pasivo
s.listen(5)  # Máximo de clientes en la cola de espera al accept()

# Bucle principal de espera por clientes
while True:
    print("Esperando un cliente")
    sd, origen = s.accept()
    print("Nuevo cliente conectado desde %s, %d" % origen)

    print("Durmiendo 1 segundo...")
    time.sleep(10)

    continuar = True
    # Bucle de atención al cliente conectado
    while continuar:
        datos = sd.recv(5)  # Observar que se lee del socket sd, no de s
        datos = datos.decode("ascii")  # Pasar los bytes a caracteres
        if datos=="":  # Si no se reciben datos, es que el cliente cerró el socket
            print("Conexión cerrada de forma inesperada por el cliente")
            sd.close()
            continuar = False
        elif datos=="FINAL":
            print("Recibido mensaje de finalización")
            sd.close()
            continuar = False
        else:
            print("Recibido mensaje: %s" % datos)

print("Cliente desconectado. Cerrando servidor.")
s.close()