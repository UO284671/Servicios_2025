import socket
import sys
import getpass
import ssl
import time
from email import message_from_bytes

host = "pop.gmail.com"
puerto = 995

def RecvReply(sock):
    respuestaBytes = sock.recv(1024)
    respuestaString = respuestaBytes.decode('utf-8', errors='ignore').strip()
    print(f" -> Respuesta: {respuestaString}")

    codeEsperado = b"+OK"
    codeRecibidoBytes = respuestaBytes[:3]

    if codeRecibidoBytes != codeEsperado:
        print(" !!! Error en la respuesta del servidor !!!")
        sys.exit(1)
    
    return respuestaBytes

# Solicitar credenciales y conexión POP3S
print("Introduzca sus credenciales de Gmail: ")
usuario = input("Usuario (correo Gmail): ")
contraseña = getpass.getpass("Contraseña (App Password): ")

print(f"1. Conectando a {host}:{puerto} ...")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(10)

contextoSSL = ssl.create_default_context()
sc = contextoSSL.wrap_socket(sock, server_hostname=host)
sc.connect((host, puerto))
print("Conexión segura (POP3S) establecida.")

RecvReply(sc)  # Saludo inicial debe de ser +OK

print("2. Autenticando usuario ...")
usuarioReciente = f"recent:{usuario}"
sc.sendall(f"USER {usuarioReciente}\r\n".encode('utf-8'))
RecvReply(sc)
sc.sendall(f"PASS {contraseña}\r\n".encode('utf-8'))
RecvReply(sc)

print("3. Consultando estado (STAT)...")
sc.sendall(b"STAT\r\n")
respuestaStat = RecvReply(sc)

# Número de mensajes disponibles
partesStat = respuestaStat.decode('ascii').split()
numCorreos = int(partesStat[1])
print(f"Mensajes disponibles: {numCorreos}")
if numCorreos == 0: 
    print("No hay nuevos correos para recibir")
else:
    print(f"4. Leyendo las cabeceras de {numCorreos} mensajes...")

    # Procesamos todos los mensajes
    for i in range(1, numCorreos + 1):
        comandoRetr = f"RETR {i}\r\n".encode('ascii')
        sc.sendall(comandoRetr)

        # NO usamos RecvReply aquí; acumulamos todo el response
        try:
            responseCompletoBytes = b""
            terminador = b"\r\n.\r\n"
            while True:
                dato = sc.recv(4096)
                if not dato:
                    break
                responseCompletoBytes += dato
                if responseCompletoBytes.endswith(terminador):
                    break

            if responseCompletoBytes.endswith(terminador):
                # Separar la línea de estado (+OK) del cuerpo
                pos = responseCompletoBytes.find(b"\r\n")
                if pos == -1:
                    print("\nERROR: No se encontró la línea de estado")
                else:
                    statusBytes = responseCompletoBytes[:pos]
                    mensajeCompletoBytes = responseCompletoBytes[pos + 2:]  # Saltar \r\n

                    statusString = statusBytes.decode('utf-8', errors='ignore').strip()
                    print(f" -> Respuesta de estado para mensaje {i}: {statusString}")

                    if not statusBytes.startswith(b"+OK"):
                        print(" !!! Error en la respuesta del servidor para RETR !!!")
                        sys.exit(1)

                    # Quitar terminador del cuerpo
                    mensajeLimpioBytes = mensajeCompletoBytes[:-len(terminador)]

                    # De-stuffing para eliminar puntos duplicados
                    lines = mensajeLimpioBytes.split(b'\r\n')
                    destuffed_lines = []
                    for line in lines:
                        if line.startswith(b'..'):
                            line = line[1:]
                        destuffed_lines.append(line)
                    mensajeLimpioBytes = b'\r\n'.join(destuffed_lines)

                    emailMensaje = message_from_bytes(mensajeLimpioBytes)

                    print(f"\n[Mensaje {i}/{numCorreos}]")
                    print(f"    Subject: {emailMensaje.get('Subject')}")
                    print(f"    From: {emailMensaje.get('From')}")
            else:
                print(f"\nERROR: MENSAJE {i} INCOMPLETO")
        except socket.timeout:
            print(f"\nERROR: Timeout al leer el mensaje {i}")
        except Exception as e:
            print(f"\nERROR en mensaje {i}: {str(e)}")

print("\n8. Cerrando sesión (QUIT)...")
sc.sendall(b"QUIT\r\n")
RecvReply(sc)
sc.close()
sock.close()