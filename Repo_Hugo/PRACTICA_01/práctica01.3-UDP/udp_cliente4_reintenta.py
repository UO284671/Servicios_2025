import socket
import sys

# Valores por defecto
ipDefecto = "localhost"
puertoDefecto = 9999
iniTimeout = 0.5 # tiempo inicial de espera para el ACK
maxTimeout = 2 # tiempo máximo de espera para el ACK

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

    numeroMensaje = 0 # contador de mensajes

    # Bucle envío continuo
    while True:
        try:
            mensaje = input("Introduzca el mensaje a enviar (para salir 'FIN'): ")

            if mensaje.upper() == "FIN":
                print("Cerrando el cliente.")
                break
            
            numeroMensaje += 1 # incremetamos el contador de mensajes
            mensajeCompleto = f"{numeroMensaje}: {mensaje}" # añadimos el ID al mensaje

            # Lógica de reintentos con timeout creciente
            actualTimeout = iniTimeout
            recibidoACK = False
            intento = 1

            while not recibidoACK and actualTimeout <= maxTimeout:
                # Realiza el envío/reenvío
                if intento > 1:
                    print(f"Reintento {intento} para mensaje número {numeroMensaje} (timeout = {actualTimeout})")

                cliente.sendto(mensajeCompleto.encode('utf-8'), direccionServidor)

                if intento == 1:
                    print(f"Enviado: `{mensajeCompleto}'")
                
                # Configura el timeout para la recepción
                cliente.settimeout(actualTimeout)

                try: 
                    # Esperamos el ACK del servidor
                    respuestaBytes, _ = cliente.recvfrom(1024)
                    respuesta = respuestaBytes.decode('utf-8')

                    if respuesta == "Ok":
                        recibidoACK = True
                        print(f"--- ACK recibido del servidor")
                    else: 
                        print(f"--- El paquete no ha sido recibido como debería")
                
                except socket.timeout:
                    actualTimeout *= 2 # doblamos el timeout para siguiente intento
                    intento += 1
                except Exception as e:
                    print(f"Error inesperado: {e}")
                    actualTimeout = maxTimeout + 1 # fuerza la salida
                    break

            if not recibidoACK and actualTimeout > maxTimeout:
                print(f"ERROR -> El servidor no ha respondido tras varios intentos. Mensaje perdido.")
                print(f"*** puede ser que el servidor esté caído.")
                cliente.close()
                sys.exit(1)

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