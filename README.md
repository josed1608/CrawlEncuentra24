# CrawlEncuentra24
Crawler para obtener información de los anuncios de propiedades en Encuentra24.

## Como setear el ambiente de desarrollo
El proyecto utiliza la librería Scrapy de Python3 para realizar el crawling. Se recomienda utilizar venv para setear el ambiente del proyeto en linux/Mac o Anaconda en Windows. Dentro del virtual environment se deben instalar Scrapy y ScrapySplash con los siguientes comandos:

  `pip install scrapy`
  
  `pip install scrapy-splash`

También se debe instalar Splash e iniciar su imagen de docker [siguiendo estas instrucciones](https://splash.readthedocs.io/en/latest/install.html)
  
## Cómo correr el crawler
Para correr el crawler se debe correr la imagen de Docker en una terminal con el comando:

`docker run -p 8050:8050 --rm --name crawler scrapinghub/splash`

Y luego en otra terminal el scrapy se inicia con el comando:

`scrapy crawl Encuentra24Spider -o info.csv`

El resultado de la corrida será un archivo de nombre `anuncios.csv` que contendrá la información obtenida de Encuentra24. Si se desea cambiar la ruta o nombre del archivo de salida, se puede hacer por medio de la variable `LOG_FILE` dentro del archivo `CrawlEncuentra24/settings.py`.