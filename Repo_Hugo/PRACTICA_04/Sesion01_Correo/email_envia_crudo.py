import socket 
import sys
import email.message, email.policy, email.utils

def RecvReply(sock, expectedCode):
    respuestaBytes = sock.recv(1024)
    respuestaString = respuestaBytes.decode('utf-8', errors='ignore').strip()
    print(f"Respuesta : {respuestaString}")

    bytesRecibidos = respuestaBytes[:3]
    if bytesRecibidos != expectedCode:
        print(f"ERROR CRÍTICO: Recibido {bytesRecibidos.decode()}")
        sys.exit(1)

    print(f"Código {bytesRecibidos.decode()} verificado.")

'''
cuerpoMensaje = """To: uo290875@uniovi.es
From: uo290875@uniovi.es
Subject: Prueba de Cliente SMTP Crudo\r\n
\r\nEste es un correo de prueba enviado directamente utilizadno SMTP y Python\r\n.\r\n"""
'''

archivoAdjunto = 'logoatc.gif'

cuerpoMensaje = email.message.EmailMessage()
cuerpoMensaje['To'] = 'Destinatario <hugofer003@gmail.com>'
cuerpoMensaje['From'] = 'Remitente <uo290875@uniovi.es>'
cuerpoMensaje['Subject'] = 'Prueba de Cliente SMTP Crudo'
cuerpoMensaje.set_content('Este es un correo de prueba enviado directamente utilizando SMTP y Python.')

with open(archivoAdjunto, 'rb') as f:
    dato = f.read()
cuerpoMensaje.add_attachment(dato, maintype='image', subtype='gif', filename=archivoAdjunto)
print("Archivo adjunto añadido.\n")

mensajeBytes = cuerpoMensaje.as_bytes()
mensajeBody = mensajeBytes + b"\r\n.,\r\n"

print("1. Conectando a 'relay.uniovi.es':25 ...")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(10)
sock.connect(('relay.uniovi.es', 25))

RecvReply(sock, b"220")
print("2. Enviando EHLO ...")
comandoHelo = b"EHLO relay.uniovi.es\r\n"
sock.sendall(comandoHelo)
RecvReply(sock, b"250") # esperado: 250 OK

print("3. Enviando MAIL ...")
mailFrom = "MAIL FROM: <uo290875@uniovi.es>\r\n".encode('ascii')
sock.sendall(mailFrom)
RecvReply(sock, b"250") # esperado: 250 OK

print("4. Enviado RCPT ...")
rcptTo = "RCPT TO: <hugofer003@gmail.com>\r\n".encode('ascii')
sock.sendall(rcptTo)
RecvReply(sock, b"250") # esperado: 250 OK

print("5. Enviando DATA ...")
sock.sendall(b"DATA\r\n")
RecvReply(sock, b"354") # esperado: 250 OK

print("6. Enviando cuerpo y finalizando ...")
sock.sendall(mensajeBody)
RecvReply(sock, b"250") # esperado: 250 OK

print("7. Enviando QUIT ...")
sock.sendall(b"QUIT\r\n")
RecvReply(sock, b"221") # esperado: 221 Bye