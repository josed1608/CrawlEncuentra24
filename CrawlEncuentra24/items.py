# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Crawlencuentra24Item(scrapy.Item):
    titulo = scrapy.Field()
    coordenadas = scrapy.Field()
    provincia = scrapy.Field()
    canton = scrapy.Field()
    distrito = scrapy.Field()
    tipo_de_anuncio = scrapy.Field()
    tipo_de_uso = scrapy.Field() 
    precio_colones = scrapy.Field() 
    precio_dolares = scrapy.Field() 
    porcentaje_rebaja = scrapy.Field() 
    metros_cuadrados_construccion = scrapy.Field()
    metros_cuadrados_lote = scrapy.Field()
    descripcion = scrapy.Field()
    habitaciones = scrapy.Field()
    bannos = scrapy.Field()
    parqueos = scrapy.Field() 
    nombre_publicador = scrapy.Field() 
    datos_publicador = scrapy.Field() 
    telefono_publicador = scrapy.Field()
    fecha_de_publicacion = scrapy.Field() 
    id_encuentra24 = scrapy.Field() 
    id_autogenerado = scrapy.Field()
    link = scrapy.Field()
    pagina = scrapy.Field()
