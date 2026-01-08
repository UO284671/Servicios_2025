# bot_repite.py
import asyncio
import logging
import ssl
import sys
import getpass
import os

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

        # -- REGISTROS PARA ESTADOS DE CHAT (EJERCICIO 8) --
        self.add_event_handler("chatstate_active", self.callback_para_activo)
        self.add_event_handler("chatstate_composing", self.callback_para_escribiendo)
        self.add_event_handler("chatstate_paused", self.callback_para_pausado)
        self.add_event_handler("chatstate_gone", self.callback_para_ausente)
        
        # Configuraciones adicionales (Extensiones)
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0004') # Data Forms
        self.register_plugin('xep_0060') # PubSub
        self.register_plugin('xep_0199') # XMPP Ping
        self.register_plugin('xep_0085') # CRÍTICO: Chat State Notifications (Ejercicio 8)

    # --- INICIO DE CALLBACKS (MÉTODOS DE LA CLASE MiBot) ---
    
    async def callback_para_session_start(self, evento):
        # Envía la presencia y solicita el roster (Ej. 6)
        self.send_presence()
        await self.get_roster()
        
        logging.info("Sesión iniciada. Bot en línea.")
        print(f"Bot '{self.jid}' conectado y esperando mensajes.")

    async def callback_para_message(self, evento):
        # Maneja los mensajes entrantes (Ej. 7)
        print("-" * 40)
        logging.info(f"Mensaje recibido de: {evento['from'].bare} (Tipo: {evento['type']})")
        logging.info(f"Contenido: {evento['body']}")
        
        # Responde solo a mensajes de tipo 'chat'
        if evento['type'] == 'chat':
            
            cuerpo_original = evento['body']
            respuesta = f"¿{cuerpo_original}?"
            
            # Envía la respuesta 'eco'
            self.send_message(
                mto=evento['from'].bare, # Destinatario: el JID sin recurso
                mbody=respuesta,
                mtype='chat'
            )
            logging.info(f"Enviado eco: {respuesta} a {evento['from'].bare}")
            
        else:
            logging.info("Mensaje ignorado (no es de tipo 'chat').")
            
        print("-" * 40)
        
    # --- CALLBACKS PARA ESTADOS DE CHAT (EJERCICIO 8) ---
    
    async def callback_para_activo(self, evento):
        jid_bare = evento["from"].bare
        print(f"{jid_bare} está activo")

    async def callback_para_escribiendo(self, evento):
        jid_bare = evento["from"].bare
        print(f"{jid_bare} está escribiendo...")

    async def callback_para_pausado(self, evento):
        jid_bare = evento["from"].bare
        print(f"{jid_bare} ha parado de escribir")
        
    async def callback_para_ausente(self, evento):
        jid_bare = evento["from"].bare
        print(f"{jid_bare} se ha ido (gone)")

# --- PROGRAMA PRINCIPAL ---

if __name__ == '__main__':
    # --- Configuración de JID y Credenciales ---
    # CAMBIA 'hugo@ingserv777' por el JID del usuario que vas a usar para el bot.
    # El usuario 'hugo' o 'cesar' que ya creaste sirve.
    BOT_JID = os.getenv("BOT_JID", "hugo@ingserv777") 
    
    servidor_ip = input("Introduce la IP del servidor Prosody (ej: localhost): ")
    servidor_port = 5222

    print(f"Introduce la contraseña para el JID {BOT_JID}")
    try:
        password = getpass.getpass()
    except Exception as e:
        print('Fallo al leer la contraseña:', e)
        sys.exit(1)
        
    # --- Configuración de Logging y Cliente ---
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)-8s %(message)s')

    cliente = MiBot(BOT_JID, password, servidor_ip)

    # CRÍTICO: Configuración SSL/TLS relajada para certificados auto-firmados
    cliente.ssl_context = ssl.create_default_context()
    cliente.ssl_context.check_hostname = False
    cliente.ssl_context.verify_mode = ssl.CERT_NONE
    
    # --- Conexión y Bucle de Eventos (Ejercicio 6) ---
    try:
        print(f"Intentando conectar a {servidor_ip}:{servidor_port}...")
        cliente.connect((servidor_ip, servidor_port))
        
        # Arrancar el bucle de eventos
        cliente.process(forever=True) 

    except KeyboardInterrupt:
        print("\nBot detenido por el usuario (Ctrl+C).")
        cliente.disconnect()
        sys.exit(0)
    except Exception as e:
        print(f"Error al conectar o procesar: {e}")
        sys.exit(1)