#!/bin/bash

# 1. Limpieza inicial de servidores
echo "Deteniendo y eliminando servidores srv1, srv2, srv3..."
docker stop srv1 srv2 srv3 2>/dev/null
docker rm srv1 srv2 srv3 2>/dev/null
docker container prune -f

# 2. Crear la red (si no existe)
docker network create pruebas 2>/dev/null

BASE_PATH=$(pwd)

# 3. Lanzar los 3 servidores broadcast
echo "Lanzando 3 servidores broadcast en la red 'pruebas'..."
docker run -d --name srv1 --network pruebas -v $BASE_PATH:/app python:3.7 python /app/udp_servidor6_broadcast.py
docker run -d --name srv2 --network pruebas -v $BASE_PATH:/app python:3.7 python /app/udp_servidor6_broadcast.py
docker run -d --name srv3 --network pruebas -v $BASE_PATH:/app python:3.7 python /app/udp_servidor6_broadcast.py

echo "Servidores lanzados. Verifique con 'docker ps'."
