# udp_cliente4.py
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
    
    # Bucle de reintentos
    confirmado = False
    timeout_actual = 0.1

    while not confirmado:
        # 1. Enviar (o reenviar) el mensaje
        print(f"Enviando: '{mensaje_final}' (Timeout: {timeout_actual}s)")
        s.sendto(mensaje_final.encode('utf-8'), (IP_SERVIDOR, PUERTO_SERVIDOR))
        
        s.settimeout(timeout_actual)
        # 2. Esperar el "OK"
        try:
            datos_ok, origen = s.recvfrom(1024)
            
            if datos_ok == b"OK":
                print("-> Confirmación (OK) recibida.")
                confirmado = True
                num_mensaje += 1
            else:
                print(f"-> Recibido algo inesperado: {datos_ok.decode('utf-8')}")
                
        except socket.timeout:
            print("-> ERROR: Timeout. El 'OK' no llegó.")
            timeout_actual *= 2  # Doblamos el timeout

            # 4. Comprobar si nos rendimos
            if timeout_actual > 2.0:
                print("ERROR FATAL: El timeout ha superado los 2 segundos.")
                print("Puede que el servidor esté caído. Abortando.")

# 4. Cerramos el socket al terminar
s.close()
print("Cliente finalizado.")