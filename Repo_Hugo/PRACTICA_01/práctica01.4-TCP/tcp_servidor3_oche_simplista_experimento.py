import socket
import sys
import time

# 1. Manejo del puerto: 9999 por defecto o por argumento
puertoDefecto = 9999

if len(sys.argv) > 2:
    print("Uso: python tcp_servidor3_oche_simplista.py <puerto>")
    sys.exit(1)

puerto = puertoDefecto
if len(sys.argv) == 2:
    try:
        puerto = int(sys.argv[1])
    except ValueError:
        print("Error: El puerto debe ser un número.")
        sys.exit(1)

print(f"Servidor TCP Oche Simplista escuchando en 0.0.0.0:{puerto}")

# Creación del socket de escucha
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", puerto)) 
s.listen(5)

# Bucle principal de espera por clientes
while True:
    print("Esperando un cliente")
    
    # Acepta la conexión
    sd, origen = s.accept()
    print("Nuevo cliente conectado desde %s:%d" % origen)
    
    # === MODIFICACIÓN CLAVE PARA EL EXPERIMENTO: time.sleep(1) ===
    time.sleep(1) 
    print("... Servidor despierta y comienza a recibir.")
    # =============================================================

    # Bucle de atención al cliente (repetir el servicio)
    while True:
        try:
            # --- Implementación del Servicio OCHE (Eco Inverso) ---
            
            # Primero recibir el mensaje del cliente
            # La elección de 80 bytes es arbitraria y simplista
            mensaje = sd.recv(80) 
            
            if not mensaje:  # Si recv() retorna cadena vacía (b''), el cliente cerró
                print("Conexión cerrada por el cliente: %s:%d" % origen)
                sd.close()
                break # Sale del bucle de atención al cliente

            mensaje = str(mensaje, "utf8") # Convertir los bytes a caracteres

            # Segundo, quitarle el "fin de línea" que son sus 2 últimos caracteres
            # Advertencia: Asume que SIEMPRE hay al menos 2 caracteres (\r\n) y que son los correctos
            linea = mensaje[:-2] 

            # Tercero, darle la vuelta (slice [::-1] invierte la cadena)
            linea = linea[::-1]

            # Finalmente, enviarle la respuesta con un fin de línea añadido
            sd.sendall(bytes(linea+"\r\n", "utf8"))
            print(f"  -> Procesado '{mensaje.strip()}'. Enviado: '{linea}\\r\\n'")

        except ConnectionResetError:
            print("Conexión reiniciada bruscamente por el cliente: %s:%d" % origen)
            sd.close()
            break
        except IndexError:
            # Captura si el mensaje es más corto que 2 bytes (no tiene \r\n)
            print(f"Error: Mensaje muy corto o incompleto del cliente: {mensaje.strip()}. Cerrando.")
            sd.close()
            break
        except Exception as e:
            print(f"Error inesperado con el cliente {origen}: {e}")
            sd.close()
            break