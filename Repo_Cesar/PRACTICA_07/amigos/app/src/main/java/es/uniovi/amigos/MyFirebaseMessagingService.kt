package es.uniovi.amigos

import android.content.Intent
import android.util.Log
import com.google.firebase.messaging.FirebaseMessagingService
import com.google.firebase.messaging.RemoteMessage

class MyFirebaseMessagingService : FirebaseMessagingService() {

    override fun onMessageReceived(remoteMessage: RemoteMessage) {
        super.onMessageReceived(remoteMessage)
        Log.d("FCM", "¡Mensaje recibido! Enviando aviso a la UI...")

        // CORRECCIÓN: Usamos el MISMO nombre que en MainActivity
        val intent = Intent("AMIGOS_UPDATE_ACTION")

        // CORRECCIÓN: Usamos setPackage para que el mensaje no salga de tu app (seguridad)
        intent.setPackage(packageName)

        // CORRECCIÓN: Usamos sendBroadcast normal (no LocalBroadcastManager)
        // para que coincida con el registerReceiver de tu Activity
        sendBroadcast(intent)
    }

    override fun onNewToken(token: String) {
        super.onNewToken(token)
        Log.d("FCM", "Nuevo token generado: $token")
    }
}