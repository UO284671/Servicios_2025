import paramiko
import time
import getpass
import sys
import logging

logging.basicConfig(stream=sys.stdout, level=logging.WARNING, 
                    format='[%(levelname)s] %(message)s')

print("Conectando al servidor ...")
password = getpass.getpass("Contraseña: ")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.WarningPolicy())
client.connect('localhost', username='alumno', password='clave-mal')
print("Conectado!!")

# Ejecutar comando remoto, redireccionando sus salidas
stdin, stdout, stderr = client.exec_command('ls')

# Mostrar resultado de la ejecución (rstrip quita los retornos de carro)
for line in stdout:
    print(line.rstrip())
time.sleep(1)  # Dar tiempo a que se vacie el buffer
client.close()
