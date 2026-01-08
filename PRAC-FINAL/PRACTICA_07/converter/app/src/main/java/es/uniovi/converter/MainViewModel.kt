package es.uniovi.converter

import android.util.Log
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.launch

class MainViewModel : ViewModel() {

    //GUARDADO DE DATOS
    //var euroToDollar: Double = 1.16
    private val _data = MutableLiveData<ConversionData>()
    val data: LiveData<ConversionData> = _data
    var yaDescargado: Boolean = false

    init {
        Log.d("MainViewModel", "ViewModel creado. Listo para trabajar.")
    }

    fun fetchExchangeRate() {
        if (yaDescargado) return

        viewModelScope.launch {
            try {
                val response = RetrofitClient.api.convert("EUR", "USD", 1.0)
                val responseBody = response.body()

                if (response.isSuccessful && responseBody != null) {
                    // Creamos el objeto del reto (Tasa + Fecha)
                    val info = ConversionData(
                        rate = responseBody.rates.USD,
                        date = responseBody.date
                    )

                    //LLAMADA PARA MOSTAR EL VALOR
                    _data.postValue(info)

                    yaDescargado = true
                    Log.d("MainViewModel", "Datos publicados en LiveData: $info")
                } else {
                    Log.e("MainViewModel", "Error: ${response.code()}")
                }
            } catch (e: Exception) {
                Log.e("MainViewModel", "Error de red", e)
            }
        }
    }
}