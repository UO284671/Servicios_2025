# tcp_cliente6_oche_len.py
import socket
import sys

IP = sys.argv[1]
PUERTO = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PUERTO))

# Abrimos el fichero en modo 'rw' (read-write)
f = s.makefile(mode='rw', encoding="utf-8", newline="\n")

print(f"Conectado a 'Oche' en {IP}:{PUERTO}. Escribe 'FIN' para salir.")

while True:
    mensaje = input(">> ")
    
    # --- Lógica de Envío ---
    longitud = "%d\n" % len(bytes(mensaje, "utf-8"))
    
    # Usamos f.write() y f.flush()
    f.write(longitud + mensaje)
    f.flush()

    if mensaje == "FIN":
        break
        
    # --- Lógica de Recepción ---
    try:
        long_resp_str = f.readline()
        if not long_resp_str:
            print("Servidor cerró la conexión.")
            break
            
        long_resp_int = int(long_resp_str.strip())
        respuesta = f.read(long_resp_int)
        
        print("Servidor dice: " + respuesta)
        
    except (ValueError, EOFError):
        print("Error leyendo la respuesta del servidor.")
        break

f.close()
s.close()
print("Conexión cerrada.")