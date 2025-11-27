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

def recibe_longitud(sock, f_like_obj):
    """
    Lee la línea de longitud del socket usando el objeto archivo 'f_like_obj'.
    Retorna la longitud (entero) o None si el socket se cierra.
    """
    try:
        # Usamos el objeto file-like para leer la línea delimitada por \n
        linea = f_like_obj.readline()
        
        if not linea: # Retorna "" si el socket se cierra
            return None
            
        # Convierte el string de la longitud a entero
        return int(linea.strip()) 
    except ValueError:
        # Si la línea no es un número válido
        return None

# Función auxiliar para enviar un mensaje con su prefijo de longitud
def envia_mensaje_con_longitud(sock, mensaje):
    """Codifica el mensaje, calcula la longitud y lo envía con el prefijo."""
    mensajeBytes = mensaje.encode("utf8")
    
    # Crear el prefijo de longitud: "%d\n" % len(...)
    longitudStr = f"{len(mensajeBytes)}\n"
    longitudPrefijo = longitudStr.encode("ascii")
    
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
    c.connect(direccionServidor)
    print("Conexión establecida.")

    # Inicializar el objeto archivo para leer la longitud de las respuestas (\n)
    f = c.makefile(encoding="ascii", newline="\n") 

    # 1. FASE DE ENVÍO: Usar la función de longitud
    print("\n--- FASE 1: ENVIANDO 3 MENSAJES CON PREFIJO DE LONGITUD ---")
    for i, msg in enumerate(mensajes):
        envia_mensaje_con_longitud(c, msg)
        print(f"  -> Enviado {i+1}: '{msg}'")

    # 2. FASE DE RECEPCIÓN: Usar la técnica de longitud para leer 3 respuestas
    print("\n--- FASE 2: RECIBIENDO 3 RESPUESTAS (USANDO LONGITUD) ---")
    for i in range(len(mensajes)):
        # a. Recibir la longitud de la respuesta
        longitud = recibe_longitud(c, f)
        
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