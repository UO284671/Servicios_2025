import email.message, email.policy, email.utils

archivoAdjunto = 'logoatc.gif'

mensaje = email.message.EmailMessage()
mensaje['To'] = 'Desti Natario <destinatario@example.com>'
mensaje['From'] = 'Remi Tente <remitente@example.com>'
mensaje['Subject'] = 'Mensaje de prueba'
mensaje['Date'] = email.utils.formatdate(localtime=True)
mensaje['Message-ID'] = email.utils.make_msgid()
mensaje.set_content("Esto es una prueba")

with open(archivoAdjunto, 'rb') as fp:
    datos = fp.read()
mensaje.add_attachment(datos, maintype='image', subtype='gif', filename=archivoAdjunto)
print(f"Adjunto {archivoAdjunto} añadido al objeto mensaje.")

binario = mensaje.as_bytes()
print(binario.decode("utf-8"))
