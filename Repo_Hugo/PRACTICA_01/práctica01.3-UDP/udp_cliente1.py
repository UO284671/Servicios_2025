import socket
import sys

# Valores por defecto
ipDefecto = "localhost"
puertoDefecto = 9999

def ejecutar():

    # Manejo de argumentos
    if len(sys.argv) == 1:
        servidor = ipDefecto
        puerto = puertoDefecto
    elif len(sys.argv) == 3:
        servidor = sys.argv[1]
        try: 
            puerto = int(sys.argv[2])
        except ValueError:
            print(f"Error: El puerto '{sys.argv[2]}' debe ser un número entero. ")
            sys.exit(1)
    else:
        print("Uso: python udp_cliente1.py <ipServidor> <puertoServidor>")
        sys.exit(1)

    # Crear el socket UDP
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(f"Cliente UDP configurado para {servidor}:{puerto}")
    except Exception as e:
        print(f"Error al crear el socket: {e}")
        sys.exit(1)

    direccionServidor = (servidor, puerto)

    # Bucle envío continuo
    while True:
        try:
            mensaje = input("Introduzca el mensaje a enviar (para salir 'FIN'): ")

            if mensaje.upper() == "FIN":
                print("Cerrando el cliente.")
                break
            
            # Envia el datagrama
            cliente.sendto(mensaje.encode('utf-8'), direccionServidor)
            print(f"Enviado: `{mensaje}'")
        
        except KeyboardInterrupt:
            print("\nCliente apagado.")
            break
        except EOFError:
            print("\nfin por EOF.")
            break
        except Exception as e:
            print(f"Error inesperado: {e}")
            break
    
    # Cerrar elsocket
    cliente.close()

if __name__ == "__main__":
    ejecutar()