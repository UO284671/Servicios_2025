#!/bin/bash
echo "Lanzando 3 servidores UDP en la red 'pruebas'..."

docker run -d --network pruebas -v $(pwd):/app python:3.7 python /app/udp_servidor6_broadcast.py
docker run -d --network pruebas -v $(pwd):/app python:3.7 python /app/udp_servidor6_broadcast.py
docker run -d --network pruebas -v $(pwd):/app python:3.7 python /app/udp_servidor6_broadcast.py

echo "Servidores lanzados. Comprueba con 'docker ps'"