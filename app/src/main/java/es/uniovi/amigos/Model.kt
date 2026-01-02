package es.uniovi.amigos

import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.PUT
import retrofit2.http.Path

//DATA CLASS
data class Amigo(
    val id: Int,
    val name: String,
    val lati: Double,
    val longi: Double
)

data class LocationPayload(
    val lati: Double,
    val longi: Double
)

data class DeviceTokenPayload(
    val device: String
)

//INTERFAZ
interface AmigosApiService {
    @GET("api/amigos")
    suspend fun getAmigos(): List<Amigo>

    //BUSCAR NOMBRE POR ID
    @GET("api/amigo/byName/{name}")
    suspend fun getAmigoByName(@Path("name") name: String): Amigo

    //ACTUALZAR POSICION
    @PUT("api/amigo/{id}")
    suspend fun updateAmigoPosition(
        @Path("id") id: Int,
        @Body payload: LocationPayload
    ): Response<Amigo>

    //ACTUALIZAR TOKEN
    @PUT("api/amigo/{id}")
    suspend fun updateAmigoDeviceToken(
        @Path("id") id: Int,
        @Body payload: DeviceTokenPayload
    ): Response<Amigo>
}

//CLIENTE RETROFIT CON LA URL DE NGROK
object RetrofitClient {
    private const val BASE_URL = "https://unsafetied-nonlactic-cara.ngrok-free.dev/"

    val api: AmigosApiService by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(AmigosApiService::class.java)
    }
}



