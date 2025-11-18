import getpass
import telnetlib

HOST = "localhost"
user = "uo284671"
password = "uo284671"

tn = telnetlib.Telnet(HOST)

tn.read_until(b"$")
tn.write(user.encode('utf-8') + b"\n")
if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('utf-8') + b"\n")

tn.write(b"ls\n")
tn.write(b"exit\n")

print(tn.read_all().decode('utf-8'))