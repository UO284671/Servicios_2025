import socket
import sys
import time # Necesario para la prueba final

# 1. Resto del servidor (basado en tcp_servidor4_oche_mejorado.py)
puertoDefecto = 9999

if len(sys.argv) > 2:
    print("Uso: python tcp_servidor5_oche_readline.py <puerto>")
    sys.exit(1)

puerto = puertoDefecto
if len(sys.argv) == 2:
    try:
        puerto = int(sys.argv[1])
    except ValueError:
        print("Error: El puerto debe ser un número.")
        sys.exit(1)

print(f"Servidor TCP Oche (readline) escuchando en 0.0.0.0:{puerto}")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", puerto)) 
s.listen(5)

while True:
    print("Esperando un cliente")
    sd, origen = s.accept()
    print("Nuevo cliente conectado desde %s:%d" % origen)
    
    time.sleep(1) 
    print("... Servidor despierta y comienza a recibir.")
    
    # === CAMBIO CLAVE 1: Inicializar el objeto archivo 'f' ===
    # El objeto 'f' usará UTF8 y buscará \r\n como separador de líneas
    f = sd.makefile(encoding="utf8", newline="\r\n") 
    # =========================================================
    
    while True:
        try:
            # === CAMBIO CLAVE 2: Usar f.readline() ===
            # f.readline() es más eficiente que recv(1) y lee hasta encontrar el delimitador \r\n
            mensaje = f.readline() 
            
            if not mensaje:  # readline() retorna "" si el cliente cerró el socket
                print("Conexión cerrada por el cliente: %s:%d" % origen)
                sd.close()
                break

            # Quitar el fin de línea, que ahora está garantizado que es \r\n
            linea = mensaje[:-2] 

            # Tercero, darle la vuelta
            linea = linea[::-1]

            # Finalmente, enviarle la respuesta con un fin de línea añadido
            sd.sendall(bytes(linea+"\r\n", "utf8"))
            print(f"  -> Procesado '{linea[::-1]}'. Enviado: '{linea}\\r\\n'")

        except Exception as e:
            print(f"Error inesperado con el cliente {origen}: {e}")
            sd.close()
            break