# tcp_cliente1.py
import socket
import sys

# 1. Obtenemos IP y Puerto de los argumentos
if len(sys.argv) == 3:
    IP = sys.argv[1]
    PUERTO = int(sys.argv[2])
else:
    print("Error: Se necesita IP y PUERTO como argumentos")
    sys.exit()

# 2. Creamos socket TCP y conectamos
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PUERTO))

print("Conectado. Escribe mensajes para enviar.")
print("La palabra 'FINAL' cierra la conexión.")

continuar = True
while continuar:
    mensaje = input(">> ")
    
    # Enviamos el mensaje
    s.send(mensaje.encode("ascii"))
    
    if mensaje == "FINAL":
        continuar = False

# 3. Cerramos socket
s.close()
print("Conexión cerrada.")