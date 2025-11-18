# tcp_servidor2_delimitador.py
import socket
import sys

PUERTO = int(sys.argv[1]) if len(sys.argv) > 1 else 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", PUERTO))
s.listen(1)

print("Servidor (con delimitador \\n) escuchando en puerto %d" % PUERTO)

while True:
    sd, origen = s.accept()
    print("Cliente conectado desde %s, %d" % origen)
    
    # Bucle de atención al cliente
    continuar = True
    while continuar:
        mensaje_recibido = ""
        while True:
            datos = sd.recv(1) 
            if not datos:
                continuar = False
                break
            
            char = datos.decode("ascii")
            
            if char == '\n':
                break
            else:
                mensaje_recibido += char
        
        if not continuar:
            print("Cliente cerró la conexión.")
        else:
            # Mensaje completo recibido
            print("Recibido: '%s'" % mensaje_recibido)
            if mensaje_recibido == "FIN":
                continuar = False
    
    # Cerramos la conexión con este cliente
    sd.close()
    print("Cliente desconectado.")

s.close()