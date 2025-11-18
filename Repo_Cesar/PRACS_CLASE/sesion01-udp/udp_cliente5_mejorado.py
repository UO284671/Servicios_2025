import socket
import sys

# Acceso a argumentos: IP y puerto por defecto localhost:9999
if len(sys.argv) == 1:
    servidor = "localhost"
    puerto = 9999
elif len(sys.argv) == 3:
    servidor = sys.argv[1]
    puerto = int(sys.argv[2])
else:
    print("Uso: python udp_cliente1.py <mensaje> <puerto>")
    sys.exit(1)

# Crear socket UDP
cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Connect para filtrar orígenes (solo del servidor)
cliente.connect((servidor, puerto))

contador = 1
while True:
    linea = input("> ")
    if linea == "FIN":
        break
    mensaje = f"{contador}: {linea}"
    
    timeout = 0.1
    exito = False
    while timeout <= 2 and not exito:
        cliente.send(mensaje.encode("utf-8"))  # send (sin to, por connect)
        cliente.settimeout(timeout)
        try:
            respuesta = cliente.recv(1024)  # recv (sin from)
            resp = respuesta.decode("utf-8")
            if resp == f"OK:{contador}":
                print("Confirmación OK")
                exito = True
        except socket.timeout:
            print(f"Timeout, reintentando...")
            timeout *= 2
    
    if not exito:
        print("Servidor caído?")
        break
    
    contador += 1

cliente.close()