# tcp_cliente3_oche.py
import socket
import sys

IP = sys.argv[1]
PUERTO = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PUERTO))

print(f"Conectado a 'Oche' en {IP}:{PUERTO}. Escribe 'FIN' para salir.")

while True:
    mensaje = input(">> ")
    
    # Enviamos el mensaje CON el delimitador \r\n
    s.sendall(bytes(mensaje + "\r\n", "utf-8"))
    
    if mensaje == "FIN":
        break
        
    # Esperamos la respuesta del servidor (el 'oche')
    respuesta = s.recv(80) # Asumimos que la respuesta cabe en 80 bytes
    
    print("Servidor dice: " + str(respuesta, "utf-8").strip()) # .strip() quita el \r\n

s.close()
print("Conexión cerrada.")