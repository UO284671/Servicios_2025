import paramiko
import getpass
import sys

host = "localhost"
user = "uo290875"
password = "Aderdal296."
port = 22

print(f"Iniciando sesión SFTP a {user}{host}:{port}")

cliente = paramiko.SSHClient()
cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
sftpCliente = None

cliente.connect(hostname=host, port=port, username=user, password=password)
print("Conexión establecida.")

sftpCliente = cliente.open_sftp()
print("Cliente SFTP abierto.")

listadoRemoto = sftpCliente.listdir()
print("Archivos de la carpeta remota: ")
for fichero in listadoRemoto:
    print(f" -{fichero}")

sftpCliente.close()
cliente.close()