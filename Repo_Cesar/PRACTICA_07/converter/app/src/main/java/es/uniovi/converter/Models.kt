package es.uniovi.converter

import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.GET
import retrofit2.http.Query

//DATA CLASSES PARA MAPEAR EL JSON
data class Rates(
    val USD: Double
)

data class ExchangeRateResponse(
    val amount: Double,
    val base: String,
    val date: String,
    val rates: Rates
)

//CLASE PARA EL EJERCICIO OPCIONAL
data class ConversionData(
    val rate: Double,
    val date: String
)

//INTERFAZ DE LA API
interface ExchangeRateApi {
    @GET("latest")
    suspend fun convert(
        @Query("from") from: String,
        @Query("to") to: String,
        @Query("amount") amount: Double
    ): Response<ExchangeRateResponse>
}

//CLIENTE DE RETROFIT
object RetrofitClient {
    private const val BASE_URL = "https://api.frankfurter.app/"

    private val retrofit by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }

    val api: ExchangeRateApi by lazy {
        retrofit.create(ExchangeRateApi::class.java)
    }
}