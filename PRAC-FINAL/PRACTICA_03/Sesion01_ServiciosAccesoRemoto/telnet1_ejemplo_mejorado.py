import getpass
import telnetlib

host = "localhost"
user = input("Introduzca su nombre de usuario: ")
password = getpass.getpass()

tn = telnetlib.Telnet(host) # Conexión

tn.read_until(b"login: ")
tn.write(user.encode('ascii') + b"\n") # Envía usuario

tn.read_until(b"Password: ")
tn.write(password.encode('ascii') + b"\n") # Envía contraseña

tn.read_until(b"$ ") # Elimina la bienvenida

tn.write(b"ls /home\n") # Ejecuta comando ls en /home
respuesta = tn.read_until(b"$ ").decode('utf-8') # Lee hasta el prompt nuevo

print(respuesta) # Muestra la salida

tn.write(b"exit\n") # Envía para cerrar sesión
tn.close()
