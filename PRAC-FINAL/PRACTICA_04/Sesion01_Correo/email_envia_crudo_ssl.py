import socket 
import sys
import email.message, email.policy, email.utils
import os
import time
import getpass 
import base64  
import ssl     

def RecvReply(sock, expectedCode):
    respuestaBytes = sock.recv(1024)
    respuestaString = respuestaBytes.decode('utf-8', errors='ignore').strip()
    print(f"Respuesta : {respuestaString}")

    bytesRecibidos = respuestaBytes[:3]
    if bytesRecibidos != expectedCode:
        print(f"ERROR CRÍTICO: Recibido {bytesRecibidos.decode()}")
        sys.exit(1)

    print(f"Código {bytesRecibidos.decode()} verificado.")

host = "smtp.gmail.com"
puerto = 587
addrFrom = "hugofer003@gmail.com"
addrTo = "hugofer003@gmail.com"
tema = "Prueba SMTP con TLS y Auth Login"
archivoAdjunto = 'logoatc.gif'

# Solicitar credenciales
print("Introduzca sus credenciales de Gmail: ")
usuario = input("Usuario (correo Gmail): ")
contraseña = getpass.getpass("Contraseña (App Password): ")

# Construcción del mensaje
print("Construyendo el mensjae...")
mensaje = email.message.EmailMessage()
mensaje['To'] = addrTo
mensaje['From'] = "Anónimo <anonimo@example.com>"
mensaje['Subject'] = tema
mensaje.set_content('Mensaje enviado a través de STARTTLS.')

with open(archivoAdjunto, 'rb') as f:
    dato = f.read()
mensaje.add_attachment(dato, maintype='image', subtype='gif', filename=archivoAdjunto)
print("Archivo adjunto añadido.\n")

mensajeBytes = mensaje.as_bytes()
mensajeBody = mensajeBytes + b"\r\n.\r\n"

print(f"1. Conectando a {host}:{puerto} (TCP)...")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(30)
sock.connect((host, puerto))

RecvReply(sock, b"220")
print("2. Enviando EHLO ...")
sock.sendall(f"EHLO {host}\r\n".encode('ascii'))
RecvReply(sock, b"250") # esperado: 250 OK

print("3. Enviando STARTTLS y negociando cifrado...")
sock.sendall(b"STARTTLS\r\n")
RecvReply(sock, b"220") # esperado: 220 Ready to start TLS

print(" -> Envolviendo el socket con SSL/TLS...")
#sc = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLS_CLIENT)
contextoSsl = ssl.create_default_context()
sc = contextoSsl.wrap_socket(sock, server_hostname=host)
print("Canal seguro (TLS) establecido.")

print("4. Iniciando AUTH LOGIN ...")
sc.sendall(b"AUTH LOGIN\r\n")
RecvReply(sc, b"334") # esperado: 334 (Servidor pide Usuario)

usuariob64 = base64.b64encode(usuario.encode('ascii'))
sc.sendall(usuariob64 + b"\r\n")
RecvReply(sc, b"334") # esperado: 334 (Servidor pide Contraseña)

passwordb64 = base64.b64encode(contraseña.encode('ascii'))
sc.sendall(passwordb64 + b"\r\n")
RecvReply(sc, b"235") # esperado: 235 Autenticación exitosa

print("5. Enviando MAIL ...")
mailFrom = f"MAIL FROM: <{addrFrom}>\r\n".encode('ascii')
sc.sendall(mailFrom)
RecvReply(sc, b"250") # esperado: 250 OK

print("6. Enviado RCPT ...")
rcptTo = f"RCPT TO: <{addrTo}>\r\n".encode('ascii')
sc.sendall(rcptTo)
RecvReply(sc, b"250") # esperado: 250 OK

print("7. Enviando DATA ...")
sc.sendall(b"DATA\r\n")
RecvReply(sc, b"354") # esperado: 250 OK

print("8. Enviando cuerpo y finalizando ...")
sc.sendall(mensajeBody)
RecvReply(sc, b"250") # esperado: 250 OK

print("9. Enviando QUIT ...")
sc.sendall(b"QUIT\r\n")
RecvReply(sc, b"221") # esperado: 221 Bye

sc.close()
sock.close()
print("Conexión cerrada. Mensaje enviado con éxito.")