import dns.resolver

respuesta = dns.resolver.query('en.wikipedia.org')
print("-- PROGRAMA EJEMPLO ---")
print(respuesta[0].address)

print("\n--- RESPUESTA DIRECTA DEL SERVIDOR ---")
print(respuesta.response)

print("\n--- RESPUESTA EN BINARIO ---")
print(respuesta.response.to_wire())