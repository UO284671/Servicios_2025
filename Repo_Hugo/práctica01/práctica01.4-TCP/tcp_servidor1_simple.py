import socket
import sys

# Manejo de puerto: 9999 por defecto
puertoDefecto = 9999

if len(sys.argv) > 2:
    print("Uso: python tcp_serviodr1_simple.py <puerto>")
    sys.exit(1)

puerto = puertoDefecto
if len(sys.argv) == 2:
    try:
        puerto = int(sys.argv[1])
    except ValueError:
        print("Error: El puerto debe de ser un número.")
        sys.exit(1)

print(f"Servidor TCP escuchando en 0.0.0.0: {puerto}")

# Creación del socket de escucha
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
# Podríamos haber omitido los parámetros, pues por defecto `socket()` en python
# crea un socket de tipo TCP

# Asignarle puerto
s.bind(("", puerto))

# Ponerlo en modo pasivo
s.listen(5)  # Máximo de clientes en la cola de espera al accept()

# Bucle principal de espera por clientes
while True:
    print("Esperando un cliente")
    sd, origen = s.accept()
    print("Nuevo cliente conectado desde %s, %d" % origen)
    continuar = True
    # Bucle de atención al cliente conectado
    while continuar:
        try:
            datos = sd.recv(5)  # Observar que se lee del socket sd, no de s
            datos = datos.decode("ascii")  # Pasar los bytes a caracteres
                    # En este ejemplo se asume que el texto recibido es ascii puro
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
        
        except ConnectionResetError:
            print("Conexión cerrada bruscamente por el cliente.")
            sd.close()
            continuar = False
        except Exception as e:
            print(f"Error inesperado con el cliente {origen}: {e}")
            sd.close()
            continuar = False