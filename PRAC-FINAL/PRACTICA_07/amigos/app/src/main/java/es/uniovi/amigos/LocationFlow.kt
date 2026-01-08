package es.uniovi.amigos

import android.annotation.SuppressLint
import android.content.Context
import android.location.Location
import android.location.LocationListener
import android.location.LocationManager
import kotlinx.coroutines.channels.awaitClose
import kotlinx.coroutines.flow.callbackFlow

// Clase para manejar resultados
sealed class LocationResult {
    data class NewLocation(val location: Location) : LocationResult()
    object PermissionDenied : LocationResult()
    object ProviderDisabled : LocationResult()
}

@SuppressLint("MissingPermission") // Los permisos se piden en la Activity
fun Context.createLocationFlow(): kotlinx.coroutines.flow.Flow<LocationResult> {
    val locationManager = getSystemService(Context.LOCATION_SERVICE) as LocationManager

    // Comprueba si el GPS está activado
    val isGpsEnabled = locationManager.isProviderEnabled(LocationManager.GPS_PROVIDER)
    if (!isGpsEnabled) {
        return kotlinx.coroutines.flow.flowOf(LocationResult.ProviderDisabled)
    }

    // callbackFlow convierte el listener antiguo en un Flow moderno
    return callbackFlow {
        val locationListener = object : LocationListener {
            override fun onLocationChanged(location: Location) {
                trySend(LocationResult.NewLocation(location))
            }
            override fun onProviderDisabled(provider: String) {
                trySend(LocationResult.ProviderDisabled)
            }
        }

        // Configuración: Actualizar cada 5s o si se mueve 10 metros
        locationManager.requestLocationUpdates(
            LocationManager.GPS_PROVIDER,
            5000L,
            10f,
            locationListener
        )

        // Limpieza al cerrar
        awaitClose {
            locationManager.removeUpdates(locationListener)
        }
    }
}