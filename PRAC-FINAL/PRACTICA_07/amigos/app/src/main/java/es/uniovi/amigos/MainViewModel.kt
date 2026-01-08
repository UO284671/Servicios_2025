package es.uniovi.amigos

import android.app.Application
import android.util.Log
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import com.google.firebase.messaging.FirebaseMessaging
import kotlinx.coroutines.tasks.await

class MainViewModel(application: Application) : AndroidViewModel(application) {

    private val _amigosList = MutableLiveData<List<Amigo>>()
    val amigosList: LiveData<List<Amigo>> = _amigosList

    // Variables para saber quién soy
    private var userName: String? = null
    private var userId: Int? = null // Al principio no sabemos el ID

    private val locationFlow = application.createLocationFlow()

    init {
        Log.d("MainViewModel", "Iniciando...")
        //startPolling()
        getAmigosList()
    }

    //1.Recibimos el nombre desde la Activity
    fun setUserName(name: String) {
        userName = name
        Log.d("MainViewModel", "Usuario: $name. Iniciando registro...")

        viewModelScope.launch {
            try {
                // 1. Buscamos el ID del usuario
                val amigo = RetrofitClient.api.getAmigoByName(name)
                userId = amigo.id
                Log.d("MainViewModel", "✅ ID Recibido: $userId")

                // 2. Obtenemos el Token de Firebase (Ejercicio 16)
                val token = FirebaseMessaging.getInstance().token.await()
                Log.d("MainViewModel", "✅ Token FCM: $token")

                // 3. Enviamos el Token al Backend (Ejercicio 17)
                val payload = DeviceTokenPayload(token)
                RetrofitClient.api.updateAmigoDeviceToken(amigo.id, payload)
                Log.d("MainViewModel", "✅ Token registrado en el servidor.")

            } catch (e: Exception) {
                Log.e("MainViewModel", "Error en registro: ${e.message}")
            }
        }
    }

    //2.Buscamos el ID en el servidor
    private fun fetchUserId(name: String) {
        viewModelScope.launch {
            try {
                val amigo = RetrofitClient.api.getAmigoByName(name)
                userId = amigo.id
                Log.d("MainViewModel", "¡IDENTIFICADO! Soy el usuario ID: $userId")
            } catch (e: Exception) {
                Log.e("MainViewModel", "Error buscando usuario. ¿Existe '$name' en la BD? Error: ${e.message}")
            }
        }
    }

    //3.Escuchamos al GPS y enviamos datos
    fun startLocationUpdates() {
        viewModelScope.launch {
            locationFlow.collect { result ->
                if (result is LocationResult.NewLocation) {
                    val loc = result.location

                    //EJERCICIO 14: ENVIAR AL SERVIDOR
                    userId?.let { idNoNulo ->
                        sendCoordinates(idNoNulo, loc.latitude, loc.longitude)
                    }

                } else if (result is LocationResult.ProviderDisabled) {
                    Log.w("GPS", "GPS desactivado")
                }
            }
        }
    }

    private fun sendCoordinates(id: Int, lat: Double, lon: Double) {
        viewModelScope.launch {
            try {
                val payload = LocationPayload(lat, lon)
                RetrofitClient.api.updateAmigoPosition(id, payload)
                Log.d("API", "✅ Posición enviada al servidor: $lat, $lon")
            } catch (e: Exception) {
                Log.e("API", "Error enviando posición: ${e.message}")
            }
        }
    }

    // Polling para ver a los demás
    private fun startPolling() {
        viewModelScope.launch {
            while (true) {
                getAmigosList()
                delay(5000)
            }
        }
    }

    fun getAmigosList() {
        viewModelScope.launch {
            try {
                val response = RetrofitClient.api.getAmigos()
                // CORRECCIÓN: Usar postValue para evitar cierres si no estamos en el hilo principal
                _amigosList.postValue(response)
            } catch (e: Exception) {
                Log.e("MainViewModel", "Error polling: ${e.message}")
            }
        }
    }
}