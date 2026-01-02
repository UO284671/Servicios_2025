import firebase_admin
from firebase_admin import credentials, messaging
import os

firebase_app = None

try:
    # Busca el json EN LA MISMA CARPETA que este archivo
    cred_path = os.path.join(os.path.dirname(__file__), "serviceAccount.json")
    if os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        firebase_app = firebase_admin.initialize_app(cred)
        print("✅ [FCM] Firebase CARGADO CORRECTAMENTE.")
    else:
        print(f"❌ [FCM] NO ENCUENTRO serviceAccount.json en {cred_path}")
except Exception as e:
    print(f"❌ [FCM] Error iniciando: {e}")

def notificar_amigos(tokens, body_mensaje):
    if not tokens or not firebase_app:
        return
    try:
        msg = messaging.MulticastMessage(
            notification=messaging.Notification(title="Amigos", body=body_mensaje),
            tokens=tokens
        )
        messaging.send_each_for_multicast(msg)
        print(f"🔔 [FCM] Notificación enviada a {len(tokens)} equipos.")
    except Exception as e:
        print(f"❌ Error enviando: {e}")