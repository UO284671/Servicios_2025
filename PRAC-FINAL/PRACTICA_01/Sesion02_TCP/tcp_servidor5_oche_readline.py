# tcp_servidor5_oche_readline.py
import socket
import sys
import time # Para el experimento final

PUERTO = int(sys.argv[1]) if len(sys.argv) > 1 else 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", PUERTO))
s.listen(1)

print("Servidor 'Oche' (con readline) escuchando en puerto %d" % PUERTO)

while True:
    sd, origen = s.accept()
    print("Cliente conectado desde %s, %d" % origen)
    
    # Convertimos el socket en un fichero
    f = sd.makefile(encoding="utf-8", newline="\r\n")

    # Bucle de atención al cliente
    while True:
        try:
            # 1. Leemos eficientemente con readline()
            mensaje = f.readline() 
            
            # Si readline() devuelve "", el cliente cerró
            if not mensaje:
                print("Cliente cerró la conexión (EOF).")
                break
                
            linea = mensaje.strip() # .strip() quita el \r\n
            
            if linea == "FIN":
                print("Cliente ha pedido finalizar.")
                break
            
            linea_invertida = linea[::-1]
            
            # Enviamos respuesta (podríamos usar f.write() pero sendall es más directo)
            sd.sendall(bytes(linea_invertida + "\r\n", "utf-8"))
            
        except (BrokenPipeError, ConnectionResetError):
            print("Cliente cerró la conexión (Error de Tubería).")
            break

    f.close() # Cerramos el "fichero"
    sd.close() # Cerramos el socket
    print("Cliente desconectado.")

s.close()