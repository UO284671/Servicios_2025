import socket
import sys
import getpass
import ssl
import time
import poplib
import email.message
import email.header
from email import message_from_bytes
from io import BytesIO 

host = "pop.gmail.com"
puerto = 995

def imprime_resumen_mensaje(msg_bytes):
    # Parsear los bytes recibidos y construir con ellos un
    # objeto EmailMessage
    msg = email.message_from_bytes(msg_bytes)
    # Extraemos las cabeceras "From" y "Subject"
    remite = msg.get("From", "<desconocido>")
    asunto = msg.get("Subject", "<sin asunto>")

    # Si estas cabeceras contienen unicode hay que decodificarlas
    # lo que es un poco enrevesado
    remite = email.header.make_header(email.header.decode_header(remite))
    asunto = email.header.make_header(email.header.decode_header(asunto))

    # Extraemos el cuerpo (este ya vendrá correctamente decodificado)
    cuerpo = msg.get_payload()

    # Pero si es multi-part, lo anterior nos retorna una lista
    # En ese caso nos quedamos con el primer elemento, que será a su
    # vez un mensaje con su propio payload
    if type(cuerpo) == list:
        parte_1 = cuerpo[0].get_payload()
        cuerpo = "---Multipart. Parte 1\n" + parte_1

    # Finalmente imprimimos un resumen, que son las cabeceras
    # extraidas y los primeros 200 caracteres del mensaje
    print("From:", remite)
    print("Subject:", asunto)
    print(cuerpo[:500])
    if len(cuerpo)>500:
        print("...[omitido]")
    print("-"*80)

# Solicitar credenciales y conexión POP3S
print("Introduzca sus credenciales de Gmail: ")
usuario = input("Usuario (correo Gmail): ")
contraseña = getpass.getpass("Contraseña (App Password): ")

pop3Mail = None
pop3Mail = poplib.POP3_SSL(host, puerto)
pop3Mail.set_debuglevel(1)

print("Autenticando usuario ...")
pop3Mail.user(f"recent:{usuario}")
pop3Mail.pass_(contraseña)
print("Autenticando exitosa")

numCorreos, tamañoTotal = pop3Mail.stat()
print(f"Mensajes disponibles (STAT): {numCorreos} ({tamañoTotal} bytes)")
if numCorreos == 0: print("No hay mensajes para leer.")

print(f"Resumen de {numCorreos} mensajes")
for i in range(1, numCorreos+1):
    print(f"Procesando mensaje {i}/{numCorreos}")

    respuestCode, lineasBytes, tamaño = pop3Mail.retr(1)
    mensajeCompletoBytes = b'\r\n'.join(lineasBytes)
    imprime_resumen_mensaje(mensajeCompletoBytes)

pop3Mail.quit()