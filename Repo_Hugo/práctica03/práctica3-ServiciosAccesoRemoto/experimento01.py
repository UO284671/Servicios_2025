import socket

def mostrar_hex(respuesta):
    hexString = ""
    for byte in respuesta:
        hexString += hex(byte)[2:].zfill(2) + " "
    print(hexString)

s = socket.socket()
s.connect(("localhost", 23))
respuesta = s.recv(1024)

print(respuesta)
mostrar_hex(respuesta)

s.close()

print("Fin del programa")
