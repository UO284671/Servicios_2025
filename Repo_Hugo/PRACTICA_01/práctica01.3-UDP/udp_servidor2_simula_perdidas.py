import socket
import sys
import random

# Definir IP y puerto por defecto
puertoDefecto = 9999
ipDefecto = "0.0.0.0" # todas las interfaces

def ejecutar():

    # Manejo de argumentos
    if len(sys.argv) > 2:
        print("Uso: python udp_servidor1.py <puerto>")
        sys.exit(1)
    
    puertoServidor = puertoDefecto
    if len(sys.argv) == 2:
        try:
            puertoServidor = int(sys.argv[1])
        except ValueEror:
            print(f"Error: El puerto '{sys.argv[1]}' debe ser un número entero. ")
            sys.exit(1)

    # Crear, enlazar e iniciar socket
    try:
        servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        servidor.bind((ipDefecto, puertoServidor)) # utiliza 0.0.0.0 para acceso externo
        print(f"Servidor UDP escuchando en {ipDefecto} : {puertoServidor}")
    except Exception as e:
        print(f"Error al iniciar el servidor: {e}")
        sys.exit(1)
    
    # Bucle de recepción continua
    while True:
        try:
            datosBytes, direccionCliente = servidor.recvfrom(1024) # recibe el datagrama (máximo 1024 bytes)
            contenido = datosBytes.decode('utf-8') # decodifica los bytes a string

            # Simuladmos la pérdida (50% probabilidad)
            if random.randint(0, 1) == 0:
                print(f"Simulando pérdida del paquete de {direccionCliente}")
            else:
                print(f"Recibido de {direccionCliente}: {contenido}")

        except KeyboardInterrupt:
            print("\nServidor apagado.")
            break
        except Exception as e:
            print(f"Error inesperado: {e}")
            break

    servidor.close()

if __name__ == "__main__":
    ejecutar()