# udp_cliente5.py
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
    
    # Preparamos el ACK que ESPERAMOS recibir (ej. "OK:1")
    ack_esperado = f"OK:{num_mensaje}".encode('utf-8')

    timeout_actual = 0.1
    while True: # Bucle de reintentos
        s.sendto(mensaje_final.encode('utf-8'), servidor)
        
        s.settimeout(timeout_actual)  
        try:
            datos, origen = s.recvfrom(1024)
            
            # VERIFICACIÓN CRÍTICA: ¿Es el ACK correcto?
            if datos == ack_esperado:
                print(f"-> Confirmación válida recibida ({datos.decode()}).")
                break # Éxito, salimos
            else:
                # Si llega un OK viejo o basura, lo mostramos pero NO salimos del bucle
                print(f"-> Ignorado paquete incorrecto: {datos.decode()}")

        except socket.timeout:
            print(f"-> Timeout ({timeout_actual}s). Reintentando...")
            timeout_actual = timeout_actual * 2
            
            if timeout_actual > 2.0:
                print("Error: Servidor no responde. Abortando.")
                break

    num_mensaje += 1

# 4. Cerramos el socket al terminar
s.close()
print("Cliente finalizado.")