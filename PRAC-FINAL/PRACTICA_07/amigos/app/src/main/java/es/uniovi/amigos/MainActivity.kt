package es.uniovi.amigos

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.os.Bundle
import android.util.Log
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import androidx.preference.PreferenceManager
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.osmdroid.config.Configuration
import org.osmdroid.tileprovider.tilesource.TileSourceFactory
import org.osmdroid.util.GeoPoint
import org.osmdroid.views.MapView
import org.osmdroid.views.overlay.Marker
import androidx.core.content.ContextCompat
import android.app.AlertDialog
import android.widget.EditText
import android.content.BroadcastReceiver
import android.content.Intent
import android.content.IntentFilter
import android.os.Build


class MainActivity : AppCompatActivity() {

    private var map: MapView? = null
    private val viewModel: MainViewModel by viewModels()

    private val requestPermissionLauncher =
        registerForActivityResult(
            ActivityResultContracts.RequestMultiplePermissions()
        ) { permissions ->
            if (permissions[Manifest.permission.ACCESS_FINE_LOCATION] == true) {
                Log.d("Permissions", "Permiso de GPS CONCEDIDO")
                // ¡AQUI ARRANCAMOS EL GPS!
                viewModel.startLocationUpdates()
            } else {
                Log.d("Permissions", "Permiso de GPS DENEGADO")
            }
        }

    private fun checkAndRequestLocationPermissions() {
        val permissionsToRequest = arrayOf(
            Manifest.permission.ACCESS_FINE_LOCATION,
            Manifest.permission.ACCESS_COARSE_LOCATION
        )

        // Comprobar si ya los tenemos
        if (permissionsToRequest.all {
                ContextCompat.checkSelfPermission(this, it) == PackageManager.PERMISSION_GRANTED
            }) {
            Log.d("Permissions", "Permisos ya concedidos. Iniciando GPS.")
            // ¡AQUI ARRANCAMOS EL GPS!
            viewModel.startLocationUpdates()
        } else {
            // Si no, los pedimos
            Log.d("Permissions", "Solicitando permisos...")
            requestPermissionLauncher.launch(permissionsToRequest)
        }
    }

    private fun askUserName() {
        val builder = AlertDialog.Builder(this)
        builder.setTitle("Identificación")
        builder.setMessage("Introduce tu nombre de usuario (ej: Cesar):")

        val input = EditText(this)
        builder.setView(input)

        builder.setPositiveButton("Aceptar") { _, _ ->
            val name = input.text.toString()
            if (name.isNotBlank()) {
                // Le pasamos el nombre al ViewModel
                viewModel.setUserName(name)
            }
        }
        // Evitamos que el usuario lo cierre sin poner nada
        builder.setCancelable(false)
        builder.show()
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        lifecycleScope.launch {
            withContext(Dispatchers.IO) {
                val ctx: Context = applicationContext
                Configuration.getInstance().load(ctx, PreferenceManager.getDefaultSharedPreferences(ctx))
            }
            setContentView(R.layout.activity_main)
            map = findViewById(R.id.map)
            map?.setTileSource(TileSourceFactory.MAPNIK)
            map?.setMultiTouchControls(true)
            centrarMapaEnEuropa()

            //EJERCICIO 6:  Cuando el ViewModel reciba datos nuevos, se ejecutará esto
            viewModel.amigosList.observe(this@MainActivity) { listaDeAmigos ->
                Log.d("MainActivity", "¡Nuevos datos recibidos! Pintando ${listaDeAmigos.size} amigos...")
                paintAmigosList(listaDeAmigos)
            }
        }

        //INICIAMOS LA CARGA
        //viewModel.getAmigosList()
        checkAndRequestLocationPermissions()
        askUserName()
    }

    //EJERCICIO 7: Pintar la lista completa
    private fun paintAmigosList(lista: List<Amigo>) {
        //LIMPIAR LAS CHINCHETAS ANTIGUAS ANTES DE PONER LAS NUEVAS
        map?.overlays?.clear()

        for (amigo in lista) {
            addMarker(amigo.lati, amigo.longi, amigo.name)
        }

        //FORZAR AL MAPA A REPINTARSE
        map?.invalidate()
    }

    //FUNCION PARA AÑADIR CHINCHETA
    private fun addMarker(latitud: Double, longitud: Double, name: String?) {
        map?.let { mapaNoNulo ->
            val startMarker = Marker(mapaNoNulo)
            startMarker.position = GeoPoint(latitud, longitud)
            startMarker.setAnchor(Marker.ANCHOR_CENTER, Marker.ANCHOR_CENTER)
            startMarker.title = name
            startMarker.snippet = "Lat: $latitud, Lon: $longitud"
            startMarker.icon = ContextCompat.getDrawable(this, R.drawable.baseline_man_24)
            mapaNoNulo.overlays.add(startMarker)
        }
    }

    //FUNCION PARA CENTRAR EL MAPA EN EUROPA
    fun centrarMapaEnEuropa() {
        val mapController = map?.controller
        mapController?.setZoom(5.5)
        val startPoint = GeoPoint(48.8583, 2.2944)
        mapController?.setCenter(startPoint)
    }

    // 1. Definimos el Receptor
    private val updateReceiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context?, intent: Intent?) {
            // AHORA LOS NOMBRES COINCIDEN
            if (intent?.action == "AMIGOS_UPDATE_ACTION") {
                Log.d("MainActivity", "🔔 ¡Aviso recibido en Activity! Recargando mapa...")

                // Pedimos la lista nueva
                viewModel.getAmigosList()
            }
        }
    }

    override fun onResume() {
        super.onResume()
        map?.onResume()

        // 2. Registramos con el nombre CORRECTO
        val filter = IntentFilter("AMIGOS_UPDATE_ACTION")

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            registerReceiver(updateReceiver, filter, Context.RECEIVER_NOT_EXPORTED)
        } else {
            registerReceiver(updateReceiver, filter)
        }
    }

    override fun onPause() {
        super.onPause()
        map?.onPause()
        // 3. Desregistramos
        unregisterReceiver(updateReceiver)
    }
}
