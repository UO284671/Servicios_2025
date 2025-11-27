import socket
import sys

# 1. Configuración de destino
ipDefecto = "127.0.0.1" 
puertoDefecto = 9999
mensajes = [
    "Hola mundo\r\n", 
    "Servicios de Red\r\n", 
    "Prueba 3\r\n"
]

if len(sys.argv) < 3:
    ipServidor = ipDefecto
    puertoServidor = puertoDefecto
else:
    ipServidor = sys.argv[1]
    try:
        puertoServidor = int(sys.argv[2])
    except ValueError:
        print("Error: El puerto debe ser un número.")
        sys.exit(1)

direccionServidor = (ipServidor, puertoServidor)

try:
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"Cliente Oche conectando a {ipServidor}:{puertoServidor}")
    c.connect(direccionServidor)
    print("Conexión establecida.")

    # 2. Bucle de envío y recepción de líneas
    for msg in mensajes:
        # Enviar la línea (ya incluye \r\n)
        datosBytes = msg.encode('utf8')
        c.sendall(datosBytes)
        print(f"  -> Enviado: '{msg.strip()}'")

        # Leer la respuesta del servidor (puede ser de hasta 80 bytes + \r\n)
        # Aquí también hay un problema de framing: recv(80) podría leer más de una respuesta
        # si la red es muy rápida, pero lo simplificamos a recv(80) como en el servidor.
        respuestaBytes = c.recv(82) 
        
        if not respuestaBytes:
            print("El servidor cerró la conexión inesperadamente.")
            break
            
        respuesta = respuestaBytes.decode('utf8').strip() # strip() quita el \r\n final
        print(f"  <- Recibido (inverso): '{respuesta}'")

except Exception as e:
    print(f"Error en el cliente: {e}")
    sys.exit(1)
finally:
    # 3. Cerrar el socket
    c.close()
    print("Socket cerrado. Cliente terminado.")