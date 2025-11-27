import socket
import sys

# Valores por defecto
puertoDefecto = 12345
timeout = 0.5 # tiempo de espera para el ACK


def ejecutar():
    
    # Manejo de argumentos
    if len(sys.argv) != 2:
        print("Uso: python udp_cliente6_broadcast.py <ip_broadcast>")
        print("Ejemplo: python udp_cliente6_broadcast.py 192.186.1.255")
        sys.exit(1)
    
    ipBroadcast = sys.argv[1]
    direccionBroadcast = (ipBroadcast, puertoDefecto)
    servidores = []

    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Configura el socket para Broadcast
        cliente.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        print(f"Cliente Broadcast. Descubriendo servidores en {ipBroadcast}:{puertoDefecto}")

    except Exception as e:
        print(f"Error al configurar el socket: {e}")
        sys.exit(1)
    

    # PASO01 : EVIAR SOLICITUD DE DESCUBRIMIENTO POR BROADCAST
    mensajeMuestra = "BUSCANDO HOLA".encode('utf-8')
    cliente.sendto(mensajeMuestra, direccionBroadcast)
    print(f"Enviado: 'BUSCANDO HOLA' a la subred.")


    # PASO02 : RECOLECTAR RESPUESTAS CON EL TIMEOUT
    cliente.settimeout(timeout)

    while True:
        try:
            respuestaBytes, (ipServidor, puertoServidor) = cliente.recvfrom(1024)
            respuesta = respuestaBytes.decode('utf-8').upper().strip()

            if respuesta == "IMPLEMENTO HOLA":
                print(f"Descubierto servidor en IP: {ipServidor}")
                # Almacenamos solo la IP para el siguiente paso
                if ipServidor not in servidores:
                    servidores.append(ipServidor)
            else:
                print(f"Recibido mensaje inesperado: {respuesta}")
        
        except socket.timeout: # suponemos que ya no se encontraron más servidores
            print(f"Descubrimiento finalizado. Se encontraron {len(servidores)} servidor(es).")
            break
    
    
    # PASO03 : PROBAR EL SERVICIO CON EL PRIMER SERVIDOR ENCONTRADO
    if servidores:
        ipServidor = servidores[0]
        print(f"*** Probando servicio 'HOLA' con {ipServidor}")

        # 3.1 Envia solicitud del servicio 'HOLA' al servidor (dirección específica)
        mensajeServicio = "HOLA".encode('utf-8')
        cliente.sendto(mensajeServicio, (ipServidor, puertoServidor))

        # 3.2 Espera la respuesta 
        try:
            cliente.settimeout(1.0) # alargamos el timeout para la respuesta final
            respuestaBytes, _ = cliente.recvfrom(1024)
            respuestaServicio = respuestaBytes.decode('utf-8')

            print(f"Respuesta del servicio 'HOLA': {respuestaServicio}")
        
        except socket.timeout:
            print(f"El servidor {ipServidor} no respondió al servicio 'HOLA' a tiempo.")
        except Exception as e: 
            print(f"Error al recibir la respuesta del servicio: {e}")
    
    else:
        print(f"No se han encontrado servidores para probar nuestro servicio 'HOLA'.")
    
    cliente.close()
    
if __name__ == "__main__":
    ejecutar()