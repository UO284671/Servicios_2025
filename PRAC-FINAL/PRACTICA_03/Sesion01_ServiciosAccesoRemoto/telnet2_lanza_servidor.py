import telnetlib
import sys
import time

host = "localhost"
port = 23
usuario = "uo290875"
password = "Aderdal296."
prompt = b"$ "
servidor = b"udp_servidor3_con_ok.py"

tn = telnetlib.Telnet(host, port)

tn.read_until(b"login: ", 1)
tn.write(usuario.encode('ascii') + b"\n")
tn.read_until(b"Password: ", 2)
tn.write(password.encode('ascii') + b"\n")

print("Autenticación realizada, esperando prompt ...")
tn.read_until(prompt, 3)

comandoPs = b"ps -ef\n"
tn.write(comandoPs)
respuestaPs = tn.read_until(prompt)
if respuestaPs.find(servidor) != -1: 
    print("El servidor ya está en ejecución.")
else: 
    print("Procediendo a lanzar el servidor ...")
    comandoServidor = b"nohup python3 " + servidor + b"\n"
    tn.write(comandoServidor)

    time.sleep(1)
    tn.read_until(prompt, 1)
    print("Servidor lanzado en segundo plano. ")

tn.write(b"exit\n")
respuestaFinal = tn.read_all().decode('utf-8', errors='ignore')

tn.close()
print("Final de sesión. Respuesta final: ", respuestaFinal)