#!/bin/bash
docker run -d --rm --network pruebas --name mariadb -e MYSQL_ROOT_PASSWORD=$DB_ROOT_PASSWORD -v $(pwd)/basedatos:/var/lib/mysql mariadb:10.11

