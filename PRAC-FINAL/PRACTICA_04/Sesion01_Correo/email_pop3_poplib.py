import socket
import sys
import getpass
import ssl
import time
import poplib
from email import message_from_bytes
from io import BytesIO 

host = "pop.gmail.com"
puerto = 995

# Solicitar credenciales y conexión POP3S
print("Introduzca sus credenciales de Gmail: ")
usuario = input("Usuario (correo Gmail): ")
contraseña = getpass.getpass("Contraseña (App Password): ")

pop3Mail = None
pop3Mail = poplib.POP3_SSL(host, puerto)
pop3Mail.set_debuglevel(2)

print("Autenticando usuario ...")
pop3Mail.user(f"recent:{usuario}")
pop3Mail.pass_(contraseña)
print("Autenticando exitosa")

numCorreos, tamañoTotal = pop3Mail.stat()
print(f"Mensajes disponibles (STAT): {numCorreos} ({tamañoTotal} bytes)")
if numCorreos == 0: print("No hay mensajes para leer.")

print(f"Solicitando mensaje 1 con RETR...")
respuestCode, lineasBytes, tamaño = pop3Mail.retr(1)

print("Extrayenco cabeceras...")
mensajeCompletoBytes = b'\r\n'.join(lineasBytes)
emailMensaje = message_from_bytes(mensajeCompletoBytes)
print(f"    Subject: {emailMensaje.get('Subject')}")
print(f"    From: {emailMensaje.get('From')}")

pop3Mail.quit()