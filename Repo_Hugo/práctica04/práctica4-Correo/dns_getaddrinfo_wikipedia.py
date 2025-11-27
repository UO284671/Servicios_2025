import socket
import sys

print("Buscando información para wikipedia.org:www")
info = socket.getaddrinfo("en.wikipedia.org", "www", socket.AF_INET, socket.SOCK_STREAM)

(family, socktype, proto, canonname, sockaddr) = info[0]

print("Parámetros de la conexión encontrados: ")
sock = None
sock = socket.socket(family, socktype, proto)
sock.settimeout(5)
sock.connect(sockaddr)
print("Conexión establecida...")

request = (
            f"GET / HTTP/1.0\r\n"
            f"Host: en.wikipedia.org\r\n"
            f"User-Agent: Python-Client/1.0\r\n"
            f"\r\n"
        )
sock.sendall(request.encode('ascii'))
print("Solicitud enviada...")

respuestaBytes = b""
while True:
    chunk = sock.recv(4096)
    if not chunk: break
    respuestaBytes += chunk
print("Repuesta del servidor:")
print(respuestaBytes.decode('utf-8', errors='ignore'))