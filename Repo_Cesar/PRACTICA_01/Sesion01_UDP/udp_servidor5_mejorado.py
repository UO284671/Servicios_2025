# udp_servidor5.py
import socket
import sys
import random

# 1. Obtenemos el puerto de los argumentos (9999 por defecto)
if len(sys.argv) > 1:
    PUERTO = int(sys.argv[1])
else:
    PUERTO = 9999

print(f"Servidor5 UDP iniciando en el puerto {PUERTO}")

# 2. Inicia la lógica del servidor5 UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 3. Enlazamos el socket al puerto
s.bind(('', PUERTO))

# Memoria para guardar los IDs de mensajes ya procesados
ids_procesados = set()

while True:
    datos, direccion = s.recvfrom(1024)
    mensaje_decodificado = datos.decode('utf-8')

    # Simulamos pérdida del 50% (para probar reintentos)
    if random.randint(1, 10) <= 5:
        print(f"[X] Simulando pérdida de: {mensaje_decodificado}")
        continue

    # Extraemos el ID del mensaje. Formato esperado: "ID: MENSAJE"
    try:
        partes = mensaje_decodificado.split(":", 1)
        msg_id = partes[0]
        texto = partes[1]
    except IndexError:
        continue # Si el mensaje no tiene formato correcto, lo ignoramos

    # Construimos la respuesta de confirmación específica
    respuesta_ack = f"OK:{msg_id}"

    # Lógica de control de duplicados
    if msg_id in ids_procesados:
        print(f"Detectado duplicado ({msg_id}). Reenviando ACK sin procesar.")
        s.sendto(respuesta_ack.encode('utf-8'), direccion)
    else:
        # Es un mensaje nuevo: Lo procesamos
        print(f"Recibido ({msg_id}): {texto.strip()}")
        ids_procesados.add(msg_id) # Guardamos el ID
        s.sendto(respuesta_ack.encode('utf-8'), direccion)
s.close()