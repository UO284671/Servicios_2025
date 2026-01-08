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

tn.write(b"ls /home\n") # Ejecuta comando ls en /home
tn.write(b"exit\n") # Envía para cerrar sesión

print(tn.read_all().decode('utf-8')) # Muestra toda la salida