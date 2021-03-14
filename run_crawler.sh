#!/bin/bash

source ~/.bashrc # para obtener acceso a los comandos de virtualenv
. $HOME/.local/bin/virtualenvwrapper.sh
workon crawler
cd ~/CrawlEncuentra24
docker run -p 8050:8050 --rm --name crawler scrapinghub/splash &
sleep 5 # para darle tiempo al docker de setearse
scrapy crawl Encuentra24Spider -o anuncios.csv
docker stop crawler