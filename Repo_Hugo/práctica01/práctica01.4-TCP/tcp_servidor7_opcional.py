import socket
import sys
import time

def recvall(sock, n):
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


# Configuraciones y socket de escucha 
puertoDefecto = 9999

if len(sys.argv) > 2:
    print("Uso: python tcp_servidor7_opcional.py <puerto>")
    sys.exit(1)

puerto = puertoDefecto
if len(sys.argv) == 2:
    try:
        puerto = int(sys.argv[1])
    except ValueError:
        print("Error: El puerto debe ser un número.")
        sys.exit(1)

print(f"Servidor TCP (Length Binary) escuchando en 0.0.0.0:{puerto}")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", puertoDefecto)) 
s.listen(5)

while True:
    print("Esperando un cliente")
    sd, origen = s.accept()
    print("Nuevo cliente conectado desde %s:%d" % origen)
    
    #time.sleep(1)
    
    while True:
        try:
            # 1. RECIBIR LA LONGITUD DEL MENSAJE
            longitud = recibe_longitud_binaria(sd)
            
            if longitud is None or longitud == 0:
                print("Conexión cerrada por el cliente o longitud nula.")
                sd.close()
                break

            # 2. RECIBIR EL CUERPO DEL MENSAJE (usando recvall)
            datosBytes = recvall(sd, longitud)
            
            if not datosBytes or len(datosBytes) != longitud:
                print("Error al recibir el cuerpo del mensaje.")
                sd.close()
                break

            mensaje = datosBytes.decode("utf8")

            # PROCESAMIENTO OCHE: darle la vuelta
            linea = mensaje[::-1] 

            # 3. ENVIAR LA RESPUESTA (usando la técnica de longitud)
            respuestaBytes = linea.encode("utf8")
            longitudRespuestaBinaria = "%d\n" % len(respuestaBytes)
            
            sd.sendall(longitudRespuestaBinaria.encode("ascii") + respuestaBytes)
            print(f"  -> Procesado '{mensaje}'. Enviada respuesta de {len(respuestaBytes)} bytes.")

        except Exception as e:
            print(f"Error con el cliente {origen}: {e}")
            sd.close()
            break