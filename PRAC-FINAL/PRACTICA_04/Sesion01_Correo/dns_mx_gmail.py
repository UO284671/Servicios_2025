import dns.resolver
import socket
import sys

dominio = "gmail.com"

mxRegistros = dns.resolver.resolve(dominio, 'MX')
resultadosMx = []
for registro in mxRegistros:
    preferencia = registro.preference
    host = registro.exchange.to_text().rstrip('.')

    respIp = dns.resolver.resolve(host, 'A')
    direccionIp = respIp[0].address
    resultadosMx.append((preferencia, host, direccionIp))

resultadosMx.sort(key=lambda x: x[0])

if resultadosMx:
    print(f"--- Servidores de Correo de {dominio} ordenados por preferencia ---")
    for preferencia, host, direccionIp in resultadosMx:
        print(f"Preferencia: {preferencia} | Host: {host} | Dirección IP: {direccionIp}")