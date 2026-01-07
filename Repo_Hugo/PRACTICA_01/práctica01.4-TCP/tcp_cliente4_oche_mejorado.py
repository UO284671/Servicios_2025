import socket
import sys
import time

# 1. Función recibe_mensaje
def recibe_mensaje(sock):
    """
    Lee bytes de un socket hasta que encuentra el final de línea (\n).
    Retorna la línea completa (incluyendo \r\n) como una cadena de bytes.
    """
    linea = b''
    while True:
        # Lee hasta 1 byte a la vez. Es ineficiente, pero garantiza la delimitación.
        try:
            byte = sock.recv(1)
        except socket.timeout:
            # Manejar timeout si está configurado en el socket
            return b'' 
            
        if not byte:
            # Conexión cerrada
            return b''

        linea += byte
        
        # Comprobar si los últimos dos bytes son \r\n (el fin de línea estándar)
        if linea.endswith(b'\r\n'):
            return linea

# 2. Resto del cliente (basado en tcp_cliente3_oche_envia_seguido.py)
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
    print(f"Cliente Oche conectando a {ipServidor}:{puertoServidor}")
    c.connect(direccionServidor)
    print("Conexión establecida.")

    # 2. FASE DE ENVÍO: Enviar los tres mensajes seguidos
    print("\n--- FASE 1: ENVIANDO 3 MENSAJES SEGUIDOS ---")
    for i, msg in enumerate(mensajes):
        dataBytes = msg.encode('utf8')
        c.sendall(dataBytes)
        print(f"  -> Enviado {i+1}: {repr(msg)}")

    # 3. FASE DE RECEPCIÓN: Intentar leer 3 respuestas
    print("\n--- FASE 2: INTENTANDO RECIBIR 3 RESPUESTAS ---")
    for i in range(contadorMensajes):
        # === CAMBIO CLAVE: Usamos recibe_mensaje() ===
        respuestaBytes = recibe_mensaje(c)
        
        if not respuestaBytes:
            print(f"ERROR: El servidor cerró la conexión al leer la respuesta {i+1}.")
            break
            
        # Usar repr() para mostrar los \r\n y si la respuesta está concatenada
        print(f"  <- Recibida respuesta {i+1} (repr): {repr(respuestaBytes.decode('utf8'))}")

except Exception as e:
    print(f"Error en el cliente: {e}")
    sys.exit(1)
finally:
    # 3. Cerrar el socket
    c.close()
    print("Socket cerrado. Cliente terminado.")