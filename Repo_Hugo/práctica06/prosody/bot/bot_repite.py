import asyncio
import logging
import ssl
import sys
import getpass # Para pedir la contraseña de forma segura

# Importa el cliente base de la librería slixmpp
from slixmpp import ClientXMPP

class MiBot(ClientXMPP):
    
    def __init__(self, jid, clave, ip_servidor):
        # 1. Llamar al constructor de la clase base
        super().__init__(jid, clave)
        
        # Guardamos la IP del servidor para usarla en la conexión
        self.ip_servidor = ip_servidor

        # 2. Registrar los callbacks para los eventos
        self.add_event_handler("session_start", self.callback_para_session_start)
        self.add_event_handler("message", self.callback_para_message)

    async def callback_para_session_start(self, evento):
            # 1. Enviar stanza de presencia "online"
            self.send_presence()
            
            # 2. Enviar stanza de petición del roster (necesario en muchos servidores)
            await self.get_roster()
            
            logging.info("Sesión iniciada. Bot en línea.")
            print(f"Bot '{self.jid}' conectado y esperando mensajes.")

    async def callback_para_message(self, evento):
        # La librería ya nos pasa un objeto 'evento' que es la stanza 'message'
        
        # 1. Mostrar información en la consola (como pide el Ejercicio 6)
        print("-" * 40)
        logging.info(f"Mensaje recibido de: {evento['from'].bare} (Tipo: {evento['type']})")
        logging.info(f"Contenido: {evento['body']}")
        
        # 2. Si el mensaje es de tipo "chat":
        if evento['type'] == 'chat':
            # a. Obtener el cuerpo del mensaje y componer la respuesta
            cuerpo_original = evento['body']
            respuesta = f"¿{cuerpo_original}?"
            
            # b. Enviar la respuesta al origen
            self.send_message(
                mto=evento['from'].bare, # Destinatario: el JID sin recurso
                mbody=respuesta,
                mtype='chat'
            )
            logging.info(f"Enviado eco: {respuesta} a {evento['from'].bare}")
        print("-" * 40)

# --- PROGRAMA PRINCIPAL ---

if __name__ == '__main__':
    # Usaremos el JID del bot, por ejemplo, bot@ingservXX (donde XX es tu número de grupo)
    # ¡Asegúrate de cambiar este JID por el que creaste para el bot!
    BOT_JID = "hugo@ingserv777" 
    
    # 1. Pedir al usuario la IP del servidor
    # (El puerto 5222 es el estándar XMPP)
    servidor_ip = input("Introduce la IP del servidor Prosody (ej: localhost): ")
    servidor_port = 5222

    # 2. Pedir al usuario su contraseña de forma segura
    print(f"Introduce la contraseña para el JID {BOT_JID}")
    try:
        password = getpass.getpass()
    except Exception as e:
        print('Fallo al leer la contraseña:', e)
        sys.exit(1)
        
    # 3. Configurar logging para ver mensajes de conexión
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)-8s %(message)s')

    # 4. Instanciar la clase MiBot
    cliente = MiBot(BOT_JID, password, servidor_ip)

    # 5. Configurar SSL para que confíe en el certificado del servidor
    # Esto es CRÍTICO para certificados auto-firmados.
    cliente.ssl_context = ssl.create_default_context()
    cliente.ssl_context.check_hostname = False
    cliente.ssl_context.verify_mode = ssl.CERT_NONE
    
    # Añadimos las extensiones necesarias para el manejo de roster
    cliente.register_plugin('xep_0030') # Service Discovery
    cliente.register_plugin('xep_0004') # Data Forms
    cliente.register_plugin('xep_0060') # PubSub
    cliente.register_plugin('xep_0199') # XMPP Ping

    # 6. Conectar el bot con el servidor
    try:
        # Nota: slixmpp usa asyncio, por eso llamamos a connect.run()
        cliente.connect((servidor_ip, servidor_port))
        
        # 7. Arrancar el bucle de eventos (process(forever=True) es la versión síncrona)
        cliente.process(forever=True) 

    except KeyboardInterrupt:
        print("\nBot detenido por el usuario.")
        cliente.disconnect()
        sys.exit(0)
    except Exception as e:
        print(f"Error al conectar o procesar: {e}")
        sys.exit(1)