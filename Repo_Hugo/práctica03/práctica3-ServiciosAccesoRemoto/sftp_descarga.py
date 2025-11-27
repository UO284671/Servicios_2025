import paramiko
import sys
import getpass
import os
from stat import S_ISDIR

host = "localhost"
user = "uo290875"
password = "Aderdal296."
port = 22

carpetaRemota = "/home/uo290875/testPractica3"
carpetaLocal = "/home/uo290875/servicios/sesion03/sesion3-ServiciosAccesoRemoto/descargasRemotas"

print(f"Iniciando sesión SFTP a {user}{host}:{port}")

if not os.path.exists(carpetaLocal):
    os.makedirs(carpetaLocal)
    print(f"Directorio local creado: {carpetaLocal}")

cliente = paramiko.SSHClient()
cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
sftpCliente = None

cliente.connect(hostname=host, port=port, username=user, password=password)
print("Conexión establecida :)")

sftpCliente = cliente.open_sftp()
listadoRemoto = sftpCliente.listdir(carpetaRemota)
print("Archivos de la carpeta {carpetaRemota}: {len(listadoRemoto)}")
contador = 0

for fichero in listadoRemoto:
    rutaRemota = os.path.join(carpetaRemota, fichero)
    rutaLocal = os.path.join(carpetaLocal, fichero)

    info = sftpCliente.stat(rutaRemota)
    if not S_ISDIR(info.st_mode):
        sftpCliente.get(rutaRemota, rutaLocal)
        print(f" Descargado: {fichero}")
        contador += 1

print(f"Descarga finalizada. Total de archivos descargados: {contador}")

sftpCliente.close()
cliente.close()