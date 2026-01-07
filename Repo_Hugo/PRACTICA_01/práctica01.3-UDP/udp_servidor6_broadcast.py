import socket
import sys
import random

# Valores por defecto
puertoBroadcast = 12345
ipServidor = "0.0.0.0"

def ejecutar():
    print(f"Iniciando servidor UDP Broadcast 'HOLA' en {ipServidor}:{puertoBroadcast}")

    try:
        servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Habilita la opción del guion para broadcast
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        servidor.bind((ipServidor, puertoBroadcast))

    except Exception as e:
        print(f"Error al configurar el socket del servidor: {e}")
        sys.exit(1)
    
    
    while True:
        try:
            datosBytes, (clienteIP, clientePuerto) = servidor.recvfrom(1024)
            contenido = datosBytes.decode('utf-8').upper().strip()

            print(f"--- Datagrama recibido de {clienteIP}:{clientePuerto} : '{contenido}'")

            # Caso01 : Respuesta a Broadcast 'HOLA'
            if contenido == "BUSCANDO HOLA":
                respuesta = "IMPLEMENTO HOLA".encode('utf-8')
                servidor.sendto(respuesta, (clienteIP, clientePuerto))
                print(f"    -> Encontrado: Respondiendo 'IMPLEMENTO HOLA'")
            # Caso02 :  Solicitud de Servicio 'HOLA'
            elif contenido == "HOLA":
                respuesta = f"HOLA: {clienteIP}".encode('utf-8')
                servidor.sendto(respuesta, (clienteIP, clientePuerto))
                print(f"    -> Respondiendo 'HOLA: {clienteIP}'")
            
            else:
                print(f"    -> Ignorando mensaje no reconocido: {contenido}")
        
        except KeyboardInterrupt:
            print("\nServidor apagado.")
            break
        except Exception as e:
            print(f"Error durante la recepción: {e}")
            break
    
    servidor.close()

if __name__ == "__main__":
    ejecutar()