package es.uniovi.converter

import android.os.Bundle
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import android.view.View
import android.widget.Toast
import android.widget.EditText
import org.json.JSONObject
import java.io.BufferedReader
import java.io.InputStreamReader
import java.net.HttpURLConnection
import java.net.URL
import android.util.Log
import androidx.activity.viewModels
import androidx.lifecycle.lifecycleScope
import kotlinx.coroutines.launch
import android.widget.TextView

class MainActivity : AppCompatActivity() {

    //DECLARACION DE VARIABLES
    var euroToDollar: Double = 1.16
    lateinit var editTextEuros: EditText
    lateinit var editTextDollars: EditText
    private val viewModel: MainViewModel by viewModels()
    lateinit var textViewInfo: TextView

    //METODO DE CREACION
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        //INICIALIZAR CON LA VISTA
        editTextEuros = findViewById(R.id.editTextEuros)
        editTextDollars = findViewById(R.id.editTextDollars)

        //ENLAZAR LA VISTA
        textViewInfo = findViewById(R.id.textViewInfo)

        //OBSERVAR EL LIVEDATA
        viewModel.data.observe(this) { info ->
            textViewInfo.text = "1 € = ${info.rate} $  (Fecha: ${info.date})"

            //Opcional: Avisar con un Toast discreto
            //Toast.makeText(this, "Datos actualizados", Toast.LENGTH_SHORT).show()
        }

        //DELEGAR CARGA DE DATOS AL VIEWMODEL
        viewModel.fetchExchangeRate()
    }

    //METODO AUXILIAR PARA LA CONVERSION
    private fun convert(source: EditText, destination: EditText, factor: Double) {
        val text = source.text.toString()
        val value = text.toDoubleOrNull()
        if (value == null) {
            destination.setText("")
            return
        }
        destination.setText((value * factor).toString())
    }

    //METODO PARA EL BOTON "TO DOLLARS"
    fun onClickToDollars(view: View) {
        val currentData = viewModel.data.value

        if (currentData != null) {
            convert(editTextEuros, editTextDollars, currentData.rate)
        } else {
            Toast.makeText(this, "Aún cargando datos...", Toast.LENGTH_SHORT).show()
        }
    }

    //METODO PARA EL BOTON "TO EUROS"
    fun onClickToEuros(view: View) {
        val currentData = viewModel.data.value

        if (currentData != null) {
            convert(editTextDollars, editTextEuros, 1.0 / currentData.rate)
        } else {
            Toast.makeText(this, "Aún cargando datos...", Toast.LENGTH_SHORT).show()
        }
    }
}
