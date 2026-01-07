import socket
import sys
import time

ipDefecto = "127.0.0.1" 
puertoDefecto = 9999
mensajes = [
    "Linea 1\r\n", 
    "Linea 2\r\n", 
    "Linea 3\r\n"
]
contadorMensajes = len(mensajes)

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
    print(f"Cliente TCP (readline) conectando a {ipServidor}:{puertoServidor}")
    c.connect(direccionServidor)
    print("Conexión establecida.")

    # === CAMBIO CLAVE 1: Inicializar el objeto archivo 'f' del socket de cliente ===
    f = c.makefile(encoding="utf8", newline="\r\n") 
    # ==============================================================================

    # FASE DE ENVÍO: Enviar los tres mensajes seguidos
    print("\n--- FASE 1: ENVIANDO 3 MENSAJES SEGUIDOS ---")
    for i, msg in enumerate(mensajes):
        datosBytes = msg.encode('utf8')
        c.sendall(datosBytes)
        print(f"  -> Enviado {i+1}: {repr(msg)}")

    # FASE DE RECEPCIÓN: Usar f.readline() para leer 3 respuestas
    print("\n--- FASE 2: RECIBIENDO 3 RESPUESTAS (USANDO readline) ---")
    for i in range(contadorMensajes):
        # === CAMBIO CLAVE 2: Usamos f.readline() ===
        respuesta = f.readline()
        
        if not respuesta:
            print(f"ERROR: El servidor cerró la conexión inesperadamente al leer la respuesta {i+1}.")
            break
            
        respuestaStrip = respuesta.strip()
        print(f"  <- Recibida respuesta {i+1} (inverso): '{respuestaStrip}'")
        
except Exception as e:
    print(f"Error en el cliente: {e}")
    
finally:
    # Es crucial cerrar el objeto archivo 'f' antes de cerrar el socket 'c' si es posible,
    # aunque en este caso, cerraremos solo el socket principal.
    c.close()
    print("\nSocket cerrado. Cliente terminado.")