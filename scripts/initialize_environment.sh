#!/bin/bash

if [ "$(basename "$PWD")" != "airflow" ]; then
    echo "You are not in the 'airflow' directory. Redirecting to the 'airflow' directory."
    cd ../airflow || exit 1
fi

sudo docker-compose build
sudo docker-compose up -d