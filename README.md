# CrawlEncuentra24
Crawler para obtener información de los anuncios de propiedades en Encuentra24.

## Como setear el ambiente de desarrollo
El proyecto utiliza la librería Scrapy de Python para realizar el crawling. Se recomienda utilizat venv para setear el ambiente del proyeto. Dentro del virtual environment se deben instalar Scrapy y ScrapySplash con los siguientes comandos: 

  `pip install scrapy`
  
  `pip install scrapy-splash`

También se debe instalar Splash e iniciar su imagen de docker [siguiendo estas instrucciones](https://splash.readthedocs.io/en/latest/install.html)
  
## Cómo correr el crawler
Para correr el crawler se debe correr el comando:

`scrapy crawl Encuentra24Spider -o info.csv`

El resultado de la corrida será un archivo de nombre `info.csv` que contendrá la información obtenida de Encuentra24