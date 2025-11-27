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

# Configuraciones y socket de escucha 
puertoDefecto = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", puertoDefecto)) 
s.listen(5)

while True:
    print("Esperando un cliente")
    sd, origen = s.accept()
    print("Nuevo cliente conectado desde %s:%d" % origen)
    
    # Inicializar el objeto archivo para leer la línea de longitud (\n)
    f = sd.makefile(encoding="ascii", newline="\n") 
    
    #time.sleep(1)
    
    while True:
        try:
            # 1. RECIBIR LA LONGITUD DEL MENSAJE
            longitud = recibe_longitud(sd, f)
            
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
            longitudRespuesta = "%d\n" % len(respuestaBytes)
            
            sd.sendall(longitudRespuesta.encode("ascii") + respuestaBytes)
            print(f"  -> Procesado '{mensaje}'. Enviada respuesta de {len(respuestaBytes)} bytes.")

        except Exception as e:
            print(f"Error con el cliente {origen}: {e}")
            sd.close()
            break