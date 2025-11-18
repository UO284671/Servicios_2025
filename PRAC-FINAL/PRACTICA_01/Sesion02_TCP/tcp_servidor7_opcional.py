# tcp_servidor7_opcional.py
import socket
import sys
import struct # Importamos struct

PUERTO = int(sys.argv[1]) if len(sys.argv) > 1 else 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", PUERTO))
s.listen(1)

print("Servidor 'Oche' (Binario) escuchando en puerto %d" % PUERTO)

while True:
    sd, origen = s.accept()
    print("Cliente conectado desde %s, %d" % origen)
    
    # Abrimos el fichero en modo 'rwb' (Read-Write-BINARY)
    f = sd.makefile(mode='rwb')

    while True:
        try:
            # 1. Leemos el header (2 bytes FIJOS)
            header_bytes = f.read(2)
            if not header_bytes:
                print("Cliente cerró (EOF en longitud).")
                break
                
            # 2. Desempaquetamos el header
            longitud_tupla = struct.unpack(">H", header_bytes)
            longitud_datos = longitud_tupla[0] # unpack devuelve una tupla
            
            # 3. Leemos EXACTAMENTE esos bytes
            mensaje_bytes = f.read(longitud_datos)
            
            if not mensaje_bytes:
                print("Cliente cerró (EOF en datos).")
                break

            mensaje = mensaje_bytes.decode("utf-8")
            if mensaje == "FIN":
                print("Cliente ha pedido finalizar.")
                break

            # 4. Lógica "Oche"
            linea_invertida = mensaje[::-1]
            linea_invertida_bytes = linea_invertida.encode("utf-8")
            
            # 5. Respondemos (con el mismo protocolo binario)
            long_resp = len(linea_invertida_bytes)
            header_resp_bytes = struct.pack(">H", long_resp) #
            
            f.write(header_resp_bytes)
            f.write(linea_invertida_bytes)
            f.flush()
            
        except (ValueError, EOFError, struct.error):
            print("Cliente cerró la conexión inesperadamente.")
            break
        except (BrokenPipeError, ConnectionResetError):
            print("Cliente cerró la conexión (Error de Tubería).")
            break

    f.close()
    sd.close()
    print("Cliente desconectado.")

s.close()