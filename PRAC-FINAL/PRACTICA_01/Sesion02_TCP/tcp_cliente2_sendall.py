# tcp_cliente2_delimitador.py
import socket
import sys

IP = sys.argv[1]
PUERTO = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PUERTO))

print("Conectado. Escribe 'FIN' para salir.")

continuar = True
while continuar:
    mensaje = input(">> ")
    
    # Añadimos el delimitador (\n) que el servidor espera
    mensaje_con_salto = mensaje + '\n'
    
    s.send(mensaje_con_salto.encode("ascii"))
    
    if mensaje == "FIN":
        continuar = False

s.close()
print("Conexión cerrada.")