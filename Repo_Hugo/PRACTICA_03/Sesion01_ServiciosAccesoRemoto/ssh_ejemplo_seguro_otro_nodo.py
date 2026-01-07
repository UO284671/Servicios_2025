import paramiko
import time
import getpass
import sys
import logging
import base64

host = "192.168.0.27"
user = "alumno"
port = 22

# Cambiar por el del compañero
base64Key = b"AAAAC3NzaC1lZDI1NTE5AAAAICAzv9urF5PR5qoRyb05JAIBYvcAr3CjsIFG2exfE7s0"
keyData = base64.b64decode(base64Key)
key = paramiko.Ed25519Key(data=keyData)

client = paramiko.SSHClient()
client.get_host_keys().add(host, "ssh-ed25519", key) 
print("Clave pública añadida")

password = getpass.getpass("Contraseña compañero: ")
client.connect(host, port=port, username=usar, password=password)
print("Conectado!!")

# Ejecutar comando remoto, redireccionando sus salidas
stdin, stdout, stderr = client.exec_command('ls')

# Mostrar resultado de la ejecución (rstrip quita los retornos de carro)
for line in stdout:
    print(line.rstrip())
time.sleep(1)  # Dar tiempo a que se vacie el buffer
client.close()
