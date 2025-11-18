# tcp_servidor4_oche_mejorado.py
import socket
import sys

# --- Función del Ejercicio 4 (Técnica eficiente byte-a-byte) ---
def recibe_mensaje(sd):
    """
    Lee byte a byte del socket (sd) hasta encontrar el delimitador \r\n.
    Usa la técnica eficiente de lista + join.
    """
    buffer_lista = []  # Usamos una lista para eficiencia
    while True:
        byte = sd.recv(1)  # Leemos byte a byte
        if not byte:
            raise EOFError("Socket cerrado por el cliente")
        
        buffer_lista.append(byte)  # Añadimos el byte a la lista
        
        # El delimitador del servicio 'oche' es \r\n
        # Por simplicidad, asumimos que \n marca el fin de línea
        if byte == b"\n":
            # Devolvemos la concatenación de todos los bytes
            return b"".join(buffer_lista)
# --- Fin de la función ---

PUERTO = int(sys.argv[1]) if len(sys.argv) > 1 else 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", PUERTO))
s.listen(1)

print("Servidor 'Oche' (byte-a-byte) escuchando en puerto %d" % PUERTO)

while True:
    sd, origen = s.accept()
    print("Cliente conectado desde %s, %d" % origen)
    
    # Bucle de atención al cliente
    while True:
        try:
            # 1. Usamos la nueva función para recibir un mensaje completo
            mensaje_bytes = recibe_mensaje(sd)
            mensaje = str(mensaje_bytes, "utf-8")

            # 2. Quitamos el \r\n (2 últimos caracteres)
            # Usamos strip() que es más robusto por si solo llega \n
            linea = mensaje.strip() 
            
            if linea == "FIN":
                print("Cliente ha pedido finalizar.")
                break
            
            # 3. Invertimos
            linea_invertida = linea[::-1]
            
            # 4. Enviamos respuesta (usamos sendall para asegurar el envío)
            sd.sendall(bytes(linea_invertida + "\r\n", "utf-8"))
            
        except EOFError:
            print("Cliente cerró la conexión (EOFError).")
            break
        except (BrokenPipeError, ConnectionResetError):
            print("Cliente cerró la conexión (Error de Tubería).")
            break

    sd.close()
    print("Cliente desconectado.")

s.close()