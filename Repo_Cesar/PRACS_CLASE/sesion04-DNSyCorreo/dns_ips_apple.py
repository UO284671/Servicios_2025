import dns.resolver

respuesta = dns.resolver.query('apple.com')
for r in respuesta:
    print(r.address)