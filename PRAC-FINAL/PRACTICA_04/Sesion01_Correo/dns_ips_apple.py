import dns.resolver
import sys

print("Iniciando cosulta DNS ...")
respuesta = dns.resolver.resolve("apple.com")
print("Direcciones IP de apple.com:")
for ip in respuesta:
    print(f"- {ip.address}")