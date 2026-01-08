import smtplib
import ssl
import getpass
import sys
import time
import email.message
import os

host = "smtp.gmail.com"
puerto = 587
addrFrom = "hugofer003@gmail.com"
addrTo = "hugofer003@gmail.com"
tema = "Prueba SMTP con TLS y Auth Login"
dato = "Este mensaje fue enviado usando la librería estándar smtplib."
archivoAdjunto = 'logoatc.gif'

# Solicitar credenciales
print("Introduzca sus credenciales de Gmail: ")
usuario = input("Usuario (correo Gmail): ")
contraseña = getpass.getpass("Contraseña (App Password): ")

# Construcción del mensaje
print("Construyendo el mensaje...")
mensaje = email.message.EmailMessage()
mensaje['To'] = addrTo
mensaje['From'] = addrFrom
mensaje['Subject'] = tema
mensaje.set_content(dato)
with open(archivoAdjunto, 'rb') as f:
    dato = f.read()
mensaje.add_attachment(dato, maintype='image', subtype='gif', filename=archivoAdjunto)
print("Archivo adjunto añadido.\n")
mensajeBytes = mensaje.as_bytes()
mensajeBody = mensajeBytes + b"\r\n.\r\n"

print(f"1. Conectando a {host}:{puerto} ...")
s = smtplib.SMTP(host, puerto)
s.set_debuglevel(1)

print("2. Negociendo STARTTLS y cifrado...")
s.starttls()

print("3. Autenticando usuario...")
s.login(usuario, contraseña)

print("4. Enviando correo...")
s.sendmail(addrFrom, [addrTo], mensajeBytes)
print("Correo enviado correctamente.")

s.quit()