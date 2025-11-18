# udp_cliente6.py (MODIFICADO PARA EJERCIICIO 7)
import socket
import sys
import time

PUERTO_DESTINO = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# --- INICIO DE LA MODIFICACIÓN ---

# Por defecto, usamos <broadcast>, pero si nos pasan un argumento, usamos esa IP
if len(sys.argv) > 1:
    IP_BROADCAST = sys.argv[1]
    print(f"Usando IP de broadcast específica: {IP_BROADCAST}")
else:
    IP_BROADCAST = '<broadcast>' # 255.255.255.255
    print("Usando IP de broadcast por defecto (<broadcast>)")

# 2. Fase de Descubrimiento
print(f"Enviando broadcast a puerto {PUERTO_DESTINO}...")
s.sendto(b"BUSCANDO HOLA", (IP_BROADCAST, PUERTO_DESTINO))

# --- FIN DE LA MODIFICACIÓN ---

print("Esperando respuestas de servidores (2 segundos)...")
s.settimeout(2.0)

servidores_encontrados = []

# Bucle para recolectar respuestas
start_time = time.time()
while True:
    try:
        # Comprobamos si ha pasado el tiempo
        if time.time() - start_time > 2.0:
            break
            
        datos, origen = s.recvfrom(1024)
        mensaje = datos.decode('utf-8')
        
        if mensaje == "IMPLEMENTO HOLA":
            print(f"-> ¡Servidor encontrado en {origen}!")
            servidores_encontrados.append(origen)
            
    except socket.timeout:
        break

# 3. Fase de Servicio
if servidores_encontrados:
    print(f"\nSe encontraron {len(servidores_encontrados)} servidores.")
    
    # Elegimos el primero de la lista
    ip_servidor, puerto_servidor = servidores_encontrados[0]
    print(f"Probando servicio con el primero: {ip_servidor}")
    
    # Enviamos el saludo directo (Unicast)
    # Importante: volvemos a setear un timeout normal para esta respuesta
    s.settimeout(2.0) 
    try:
        s.sendto(b"HOLA", (ip_servidor, puerto_servidor))
        
        respuesta, _ = s.recvfrom(1024)
        print(f"Respuesta final del servidor: {respuesta.decode('utf-8')}")
        
    except socket.timeout:
        print("Error: El servidor elegido no respondió al saludo final.")
else:
    print("No se encontraron servidores activos.")

s.close()