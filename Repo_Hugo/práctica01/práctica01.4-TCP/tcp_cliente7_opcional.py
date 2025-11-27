import socket
import sys
import time

def recvall(sock, n):
    """
    Recibe exactamente 'n' bytes del socket 'sock', garantizando la lectura completa.
    Retorna un string de bytes con los datos recibidos o b'' si la conexión se cierra.
    """
    data = b''
    bytesRestantes = n
    while bytesRestantes > 0:
        chunk = sock.recv(bytesRestantes) 
        if not chunk:
            return b''
        data += chunk
        bytesRestantes -= len(chunk)
    return data

def recibe_longitud_binaria(sock):
    """
    Lee exactamente 2 bytes del socket y los decodifica como un entero Big Endian ('>H').
    Retorna la longitud (entero) o None si el socket se cierra.
    """

    # Leer los 2 bytes que contienen la longitud
    longBytes = recvall(sock, 2)
    
    if len(longBytes) < 2:
        return None # Conexión cerrada o datos insuficientes
        
    # Desempaquetar los 2 bytes: > (Big Endian), H (unsigned short - 2 bytes)
    # Retorna una tupla, tomamos el primer elemento [0]
    return struct.unpack(">H", longBytes)[0]


# Función auxiliar para enviar un mensaje con su prefijo de longitud
def envia_mensaje_con_longitud_binaria(sock, mensaje):
    """Codifica el mensaje, calcula la longitud y lo envía con el prefijo."""
    mensajeBytes = mensaje.encode("utf8")
    
    # 1. Codificar la longitud en 2 bytes Big Endian (>H)
    # Se limita a 65535 bytes (2^16 - 1)
    longitudPrefijo = struct.pack(">H", len(mensajeBytes))
    
    # Enviar la concatenación (prefijo + cuerpo)
    sock.sendall(longitudPrefijo + mensajeBytes)

# Configuraciones y conexión del socket
ipDefecto = "127.0.0.1" 
puertoDefecto = 9999
mensajes = ["Linea 1", "Linea 2", "Linea 3"]

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
    print(f"Cliente TCP (Length Binary) conectando a {servidor_ip}:{servidor_port}")
    c.connect(direccionServidor)
    print("Conexión establecida.")

    # 1. FASE DE ENVÍO: Usar la función de longitud
    print("\n--- FASE 1: ENVIANDO 3 MENSAJES CON PREFIJO DE LONGITUD ---")
    for i, msg in enumerate(mensajes):
        envia_mensaje_con_longitud_binaria(c, msg)
        print(f"  -> Enviado {i+1}: '{msg}'")

    # 2. FASE DE RECEPCIÓN: Usar la técnica de longitud para leer 3 respuestas
    print("\n--- FASE 2: RECIBIENDO 3 RESPUESTAS (USANDO LONGITUD) ---")
    for i in range(len(mensajes)):
        # a. Recibir la longitud de la respuesta
        longitud = recibe_longitud_binaria(c)
        
        if longitud is None:
            print(f"ERROR: Servidor cerró al esperar la longitud de la respuesta {i+1}.")
            break

        # b. Recibir el cuerpo de la respuesta
        respuestaBytes = recvall(c, longitud)
        
        if not respuestaBytes or len(respuestaBytes) != longitud:
            print(f"ERROR: Fallo al recibir el cuerpo de la respuesta {i+1}.")
            break

        respuesta = respuestaBytes.decode("utf8")
        print(f"  <- Recibida respuesta {i+1} (inversa, {longitud} bytes): '{respuesta}'")
        
except Exception as e:
    print(f"Error en el cliente: {e}")
    
finally:
    c.close()
    print("\nSocket cerrado. Cliente terminado.")