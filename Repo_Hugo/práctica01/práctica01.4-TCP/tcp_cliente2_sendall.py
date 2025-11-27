import socket
import sys
import time 

# Confiugración de destino.
ipDefecto = "127.0.0.1"
puertoDefecto = 9999
contadorMensajes = 5
mensjaeEnviado = "ABCD"

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
    # Crear socket TCP
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conexión con el servidor
    print(f"Cliente TCP conectado a {ipServidor}:{puertoServidor}")
    c.connect(direccionServidor)
    print("Conexión establecida.")

    # Enviar 5 veces el mensaje por defecto de 5 bytes
    print(f"Iniciando {contadorMensajes} evíos de 5 bytes...")
    for i in range(contadorMensajes):
        dataBytes = mensjaeEnviado.encode('ascii')
        c.sendall(dataBytes)
        print(f"  -> Enviado {i+1}: '{mensjaeEnviado}'")
        time.sleep(0.05)
    
    # Eviar mensaje de finalización
    mensajeFinal = "FINAL"
    print(f"Enviando mensaje de finalización: '{mensajeFinal}'")
    c.sendall(mensajeFinal.encode('ascii'))

except Exception as e:
    print(f"Error en el cliente: {e}")
    sys.exit(1)
finally:
    # Cierra el socket
    c.close()
    print("Socket cerrado. Cliente terminado.")