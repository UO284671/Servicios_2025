#!/bin/bash

# Obtenemos la IP de broadcast de la red 'pruebas'
SUBNET=$(docker network inspect pruebas -f '{{(index .IPAM.Config 0).Subnet}}')

if [ -z "$SUBNET" ]; then
  echo "Error: No se pudo encontrar la red 'pruebas' o su subnet."
  exit 1
fi

# Calculamos la IP de Broadcast (ej: 172.18.0.0/16 -> 172.18.255.255)
IP_BASE=$(echo $SUBNET | cut -d'.' -f1,2)
BROADCAST_IP="${IP_BASE}.255.255"

echo "Subred detectada: $SUBNET"
echo "IP de Broadcast calculada: $BROADCAST_IP"
echo "Lanzando cliente..."

# Lanzamos el cliente pasándole la IP calculada
docker run -it --rm --network pruebas -v $(pwd):/app python:3.7 python /app/udp_cliente7_ej6mod.py $BROADCAST_IP

# El --rm hace que el contenedor se borre solo al terminar