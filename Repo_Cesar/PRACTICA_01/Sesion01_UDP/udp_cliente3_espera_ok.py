# udp_cliente3.py
import socket
import sys

# 1. Obtenemos la IP y Puerto del servidor de los argumentos
if len(sys.argv) == 3:
    IP_SERVIDOR = sys.argv[1]
    PUERTO_SERVIDOR = int(sys.argv[2])
elif len(sys.argv) == 2:
    IP_SERVIDOR = sys.argv[1]
    PUERTO_SERVIDOR = 9999
else:
    IP_SERVIDOR = 'localhost'
    PUERTO_SERVIDOR = 9999

# 2. Logica del cliente UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor = (IP_SERVIDOR, PUERTO_SERVIDOR)

# 3. Bucle principal para enviar mensajes
print(f"Enviando mensajes a {IP_SERVIDOR}:{PUERTO_SERVIDOR}")
print("Escribe 'FIN' para terminar.")

num_mensaje = 1
while True:
    mensaje = input("Mensaje: ")
    
    if mensaje == "FIN":
        break

    # Añadimos el número de secuencia al mensaje
    mensaje_final = f"{num_mensaje}: {mensaje}"  
    s.sendto(mensaje_final.encode('utf-8'), (IP_SERVIDOR, PUERTO_SERVIDOR))
    
    # 2. Esperar el "OK"
    s.settimeout(0.1)
    try:
        datos_ok, origen = s.recvfrom(1024)
        
        if datos_ok == b"OK":
            print("-> Confirmación (OK) recibida.")
        else:
            print(f"-> Recibido algo inesperado: {datos_ok.decode('utf-8')}")
            
    except socket.timeout:
        print("-> ERROR: Timeout. El 'OK' no llegó (paquete perdido).")
    
    num_mensaje += 1

# 4. Cerramos el socket al terminar
s.close()
print("Cliente finalizado.")