import socket
import sys

# Definimos la función recvall() para asegurar la lectura completa de todos los bytes
def recvall(sock, n):
    # Recibe exáctamente n bytes del socket sock.
    mensaje = b''
    bytesRestante = n

    while bytesRestante > 0:
        # Intenta recibir los bytes restantes
        chunk = sock.recv(bytesRestante)
        data = b''

        if not chunk:
            # Si se recibe una cadena vacía, el socket está cerrado
            return b''
        
        # Concatena los bytes recibidos y actualiza el contador
        data += chunk
        bytesRestante -= len(chunk)
    
    return data

puertoDefecto = 9999

if len(sys.argv) > 2:
    print("Uso: python tcp_servidor2_recvall.py <puerto>")
    sys.exit(1)

puerto = puertoDefecto
if len(sys.argv) == 2:
    try:
        puerto = int(sys.argv[1])
    except ValueError:
        print("Error: El puerto debe ser un número.")
        sys.exit(1)

print(f"Servidor TCP (recvall) escuchando en 0.0.0.0:{puerto}")

# Configuración del socket de escucha
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", puerto)) 
s.listen(5)

# Bucle principal de espera por clientes
while True:
    print("Esperando un cliente")
    sd, origen = s.accept()
    print("Nuevo cliente conectado desde %s:%d" % origen)
    
    continuar = True
    
    # Bucle de atención al cliente conectado
    while continuar:
        try:
            # Usamos recvall() en lugar de sd.recv(5) 
            # recvall garantiza que recibiremos 5 bytes completos, o b'' si la conexión se cierra.
            datosBytes = recvall(sd, 5) 
            
            if not datosBytes:  # Si bytes es b'', el socket se cerró
                print("Conexión cerrada por el cliente: %s:%d" % origen)
                sd.close()
                continuar = False
                continue

            datos = datosBytes.decode("ascii")

            if datos == "FINAL":
                print("Recibido mensaje de finalización. Cerrando conexión con %s:%d" % origen)
                sd.close()
                continuar = False
            else:
                print("Recibido mensaje: %s" % datos)
        
        except ConnectionResetError:
            print("Conexión reiniciada/cerrada bruscamente por el cliente: %s:%d" % origen)
            sd.close()
            continuar = False
        except Exception as e:
            print(f"Error inesperado con el cliente {origen}: {e}")
            sd.close()
            continuar = False