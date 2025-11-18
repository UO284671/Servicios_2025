# tcp_servidor6_oche_len.py
import socket
import sys

PUERTO = int(sys.argv[1]) if len(sys.argv) > 1 else 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", PUERTO))
s.listen(1)

print("Servidor 'Oche' (con prefijo de longitud) escuchando en %d" % PUERTO)

while True:
    sd, origen = s.accept()
    print("Cliente conectado desde %s, %d" % origen)
    
    # Abrimos el fichero en modo 'rw' (read-write)
    f = sd.makefile(mode='rw', encoding="utf-8", newline="\n")

    while True:
        try:
            longitud_str = f.readline()
            if not longitud_str:
                print("Cliente cerró (EOF en longitud).")
                break
                
            longitud_datos = int(longitud_str.strip())
            mensaje = f.read(longitud_datos)
            
            if not mensaje or mensaje == "FIN":
                print("Cliente ha pedido finalizar.")
                break

            linea_invertida = mensaje[::-1]
            
            # Preparamos y escribimos la respuesta usando 'f'
            longitud_resp_str = "%d\n" % len(bytes(linea_invertida, "utf-8"))
            f.write(longitud_resp_str + linea_invertida)
            f.flush() # ¡Importante! Forzamos el envío
            
        except (ValueError, EOFError):
            print("Cliente cerró la conexión inesperadamente.")
            break
        except (BrokenPipeError, ConnectionResetError):
            print("Cliente cerró la conexión (Error de Tubería).")
            break

    f.close()
    sd.close()
    print("Cliente desconectado.")

s.close()