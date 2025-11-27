import socket
import sys
import time # No se usa en la versión normal, pero se añade para la prueba posterior

# 1. Función recibe_mensaje
def recibe_mensaje(sock):
    """
    Lee bytes de un socket hasta que encuentra el final de línea (\n).
    Retorna la línea completa (incluyendo \r\n) como una cadena de bytes.
    """
    linea = b''
    while True:
        # Lee hasta 1 byte a la vez. Es ineficiente, pero garantiza la delimitación.
        try:
            byte = sock.recv(1)
        except socket.timeout:
            # Manejar timeout si está configurado en el socket
            return b'' 
            
        if not byte:
            # Conexión cerrada
            return b''

        linea += byte
        
        # Comprobar si los últimos dos bytes son \r\n (el fin de línea estándar)
        if linea.endswith(b'\r\n'):
            return linea

# 2. Resto del servidor (basado en tcp_servidor3_oche_simplista.py)
puertoDefecto = 9999

if len(sys.argv) > 2:
    print("Uso: python tcp_servidor4_oche_mejorado.py <puerto>")
    sys.exit(1)

puerto = puertoDefecto
if len(sys.argv) == 2:
    try:
        puerto = int(sys.argv[1])
    except ValueError:
        print("Error: El puerto debe ser un número.")
        sys.exit(1)

print(f"Servidor TCP Oche Mejorado (recv_mensaje) escuchando en 0.0.0.0:{puerto}")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", puerto)) 
s.listen(5)

while True:
    print("Esperando un cliente")
    sd, origen = s.accept()
    print("Nuevo cliente conectado desde %s:%d" % origen)
    
    time.sleep(1) 
    print("... Servidor despierta y comienza a recibir.")
    
    while True:
        try:
            # CAMBIO CLAVE: Usamos recibe_mensaje()
            datosBytes = recibe_mensaje(sd) 
            
            if not datosBytes:  # Si retorna b'', el socket se cerró
                print("Conexión cerrada por el cliente: %s:%d" % origen)
                sd.close()
                break

            mensaje = datosBytes.decode("utf8")
            
            # El mensaje ya contiene \r\n, por lo que lo quitamos
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