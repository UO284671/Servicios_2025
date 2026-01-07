#!/bin/bash

# IP de broadcast específica de tu subred Docker (172.18.0.0/16)
IP_DE_BROADCAST="172.18.255.255" 

BASE_PATH=$(pwd)

echo "Ejecutando cliente broadcast contra: $IP_DE_BROADCAST"

# Limpieza del contenedor cliente anterior
docker rm cliente 2>/dev/null

# Lanzar el cliente en modo interactivo
docker run -it --network pruebas --name cliente -v $BASE_PATH:/app python:3.7 \
   python /app/udp_cliente6_broadcast.py $IP_DE_BROADCAST
