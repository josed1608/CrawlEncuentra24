import scrapy
from scrapy_splash import SplashRequest

from ..items import Crawlencuentra24Item

class Ecncuentra24Spider(scrapy.Spider):
    name = 'Encuentra24Spider'
    start_urls = ['https://www.encuentra24.com/costa-rica-en/searchresult/real-estate-for-sale#search=f_currency.crc&regionslug=san-jose-san-jose-capital&page=1']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse, meta={
                'splash': {
                    'endpoint': 'render.html',
                    'args': {'wait': 1}
                }
            })

    def parse(self, response):
        anuncios = Crawlencuentra24Item()

        todosLosAnuncions = response.css("article")

        for anuncio in todosLosAnuncions:
            anuncios['titulo'] = anuncio.css("strong::text").extract()
            anuncios['ubicacion'] = anuncio.css(".ann-info-item::text").extract()
            anuncios['precio'] = anuncio.css(".ann-price-2nd div::text").extract()
            anuncios['metrosCuadrados'] = anuncio.css(".icon-area+ .value::text").extract()
            anuncios['habitaciones'] = anuncio.css(".icon-category-home+ .value::text").extract()
            anuncios['descripcion'] = anuncio.css(".ann-box-desc::text").extract()

            linkAnuncio = anuncio.css(".ann-box-title::attr(href)").get()

            yield SplashRequest()

            yield anuncios