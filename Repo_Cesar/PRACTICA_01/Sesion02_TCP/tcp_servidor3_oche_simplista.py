# tcp_servidor3_oche_simplista.py
import socket
import sys

PUERTO = int(sys.argv[1]) if len(sys.argv) > 1 else 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", PUERTO))
s.listen(1)

print("Servidor 'Oche' Simplista escuchando en puerto %d" % PUERTO)

while True:
    sd, origen = s.accept()
    print("Cliente conectado desde %s, %d" % origen)
    
    # Bucle de atención al cliente conectado
    while True:
        
        # Primero recibir el mensaje del cliente
        mensaje = sd.recv(80)  # Nunca enviará más de 80 bytes
        mensaje = str(mensaje, "utf-8") # Convertir los bytes a caracteres
        
        # Segundo, quitarle el "fin de línea" que son sus 2 últimos caracteres
        linea = mensaje[:-2]  # slice desde el principio hasta el final -2
        
        if linea == "FIN":
            print("Cliente ha pedido finalizar.")
            break

        # Tercero, darle la vuelta
        linea = linea[::-1]
        
        # Finalmente, enviarle la respuesta con un fin de línea añadido
        # Observa la transformación en bytes para enviarlo
        sd.sendall(bytes(linea+"\r\n", "utf-8"))

    sd.close()
    print("Cliente desconectado.")

s.close()