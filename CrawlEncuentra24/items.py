# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Crawlencuentra24Item(scrapy.Item):
    titulo = scrapy.Field()
    ubicacion = scrapy.Field()
    precio = scrapy.Field()
    metrosCuadrados = scrapy.Field()
    habitaciones = scrapy.Field()
    descripcion = scrapy.Field()
    telefono = scrapy.Field()
    coordenadas = scrapy.Field()
    bannos = scrapy.Field()
