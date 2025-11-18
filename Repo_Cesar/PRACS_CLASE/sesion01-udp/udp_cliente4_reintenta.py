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

contador = 1
print("Escribe mensajes. 'FIN' para salir.")
while True:
    linea = input("> ")
    if linea == "FIN":
        break
    mensaje = f"{contador}: {linea}"
    
    timeout = 0.1  # Inicial
    exito = False
    while timeout <= 2 and not exito:
        cliente.sendto(mensaje.encode("utf-8"), (servidor, puerto))
        cliente.settimeout(timeout)
        try:
            respuesta, _ = cliente.recvfrom(1024)
            resp = respuesta.decode("utf-8")
            if resp == "OK":
                print("Recibida confirmación")
                exito = True
            else:
                print("Respuesta inesperada")
        except socket.timeout:
            print(f"Timeout ({timeout}s), reintentando...")
            timeout *= 2  # Duplicar
        except:
            raise
    
    if not exito:
        print("Puede que el servidor esté caído. Inténtelo más tarde.")
        break
    
    contador += 1

cliente.close()