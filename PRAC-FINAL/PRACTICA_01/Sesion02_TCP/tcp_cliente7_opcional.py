# tcp_cliente7_opcional.py
import socket
import sys
import struct # Importamos struct

IP = sys.argv[1]
PUERTO = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PUERTO))

# Abrimos el fichero en modo 'rwb' (Read-Write-BINARY)
f = s.makefile(mode='rwb')

print(f"Conectado a 'Oche' en {IP}:{PUERTO}. Escribe 'FIN' para salir.")

while True:
    mensaje = input(">> ")
    mensaje_bytes = mensaje.encode("utf-8")
    
    # --- Lógica de Envío Binaria ---
    # 1. Calculamos longitud y la "empaquetamos"
    longitud = len(mensaje_bytes)
    header_bytes = struct.pack(">H", longitud) #
    
    # 2. Enviamos header (2 bytes) + mensaje
    f.write(header_bytes)
    f.write(mensaje_bytes)
    f.flush()

    if mensaje == "FIN":
        break
        
    # --- Lógica de Recepción Binaria ---
    try:
        # 1. Leemos el header (2 bytes)
        header_resp_bytes = f.read(2)
        if not header_resp_bytes:
            print("Servidor cerró la conexión.")
            break
            
        # 2. Desempaquetamos
        long_resp_tupla = struct.unpack(">H", header_resp_bytes) #
        long_resp = long_resp_tupla[0]
        
        # 3. Leemos la respuesta
        respuesta_bytes = f.read(long_resp)
        
        print("Servidor dice: " + respuesta_bytes.decode("utf-8"))
        
    except (ValueError, EOFError, struct.error):
        print("Error leyendo la respuesta del servidor.")
        break

f.close()
s.close()
print("Conexión cerrada.")