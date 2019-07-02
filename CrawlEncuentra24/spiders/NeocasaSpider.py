import scrapy

from ..items import Crawlencuentra24Item

class NeocasaSpider(scrapy.Spider):
    name = 'NeocasaSpider'
    start_urls = ['https://www.c21neocasa.com/propiedades-en-venta/?b=2&q=costa-rica+san-jose+san-jose&ord=date-desc&r=&page=1&numberOfElements=12&v=c']

    def parse(self, response):
        anuncios = Crawlencuentra24Item()

        todosLosAnuncions = response.css(".col-lg-3")

        for anuncio in todosLosAnuncions:
            anuncios['titulo'] = anuncio.css(".title-link::text").extract()
            anuncios['ubicacion'] = anuncio.css("h4::text").extract()
            anuncios['precio'] = anuncio.css(".property-price strong::text").extract()
            anuncios['metrosCuadrados'] = anuncio.css(".mright10:nth-child(1)::text").extract()
            anuncios['habitaciones'] = anuncio.css(".mright10 strong::text").extract()
            anuncios['descripcion'] = anuncio.css("h3::text").extract()

            yield anuncios