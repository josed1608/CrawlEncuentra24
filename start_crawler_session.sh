#!/bin/bash

# Borrar los resultados de la corrida anterior
cd ~/CrawlEncuentra24
rm -f scrapy_output.txt
rm -f anuncios.csv

# Correr en una nueva ventana el crawler para poder cerrar la sesión de ssh sin matar el proceso
screen -S crawler -dm ./run_crawler.sh # `screen -r crawler` para conectarse a la terminal donde queda corriendo (Alt+A y Alt+D para desconectarse). La sesión de screen se cierra cuando el crawler termina.