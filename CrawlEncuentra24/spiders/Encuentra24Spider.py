import scrapy
import pudb
from scrapy import Request
from scrapy_splash import SplashRequest
import re

from ..items import Crawlencuentra24Item

class Ecncuentra24Spider(scrapy.Spider):
    name = 'Encuentra24Spider'
    start_urls = ['https://www.encuentra24.com/costa-rica-en/searchresult/real-estate-for-sale.1?regionslug=san-jose-san-jose-capital&q=f_currency.crc']
    BASE_URL = 'https://www.encuentra24.com'
    reg_ex_coordenadas = re.compile(r"q=-?\d+\.\d+,-?\d+\.\d+")
    archivo = True
    first_page = True

    lua_script_paginar = '''
function main(splash, args)
  assert(splash:go(args.url))
  wait_for_element(splash, '.filter_refine_tag_container', 200)
  return splash:html()
end

function wait_for_element(splash, css, maxwait)
    if maxwait == nil then
        maxwait = 10
    end
    local exit = false
    local time_chunk = 0.2
    local time_passed = 0
    while (exit == false)
    do
        local element = splash:select(css)
        if element then
            exit = true
        elseif time_passed >= maxwait then
            exit = true
            error('Timed out waiting for -' .. css)
        else
            splash:wait(time_chunk)
            time_passed = time_passed + time_chunk
        end
    end
end'''

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, endpoint='execute', args={'lua_source': self.lua_script_paginar})

    def parse(self, response):
        todos_los_anuncions = response.css("article")

        for anuncio in todos_los_anuncions:
            item_anuncio = Crawlencuentra24Item()

            item_anuncio['titulo'] = anuncio.css("strong::text").extract()
            item_anuncio['ubicacion'] = anuncio.css(".ann-info-item::text").extract()
            item_anuncio['precio'] = anuncio.css(".ann-price-2nd div::text").extract()
            item_anuncio['metrosCuadrados'] = anuncio.css(".icon-area+ .value::text").extract()
            item_anuncio['habitaciones'] = anuncio.css(".icon-category-home+ .value::text").extract()

            link_anuncio = anuncio.css(".ann-box-title::attr(href)").get()

            yield Request(url=self.BASE_URL + link_anuncio, callback=self.parse_anuncio, meta={"anuncio":  item_anuncio})

        flechas_sig_pag = response.css("nav li.arrow a::attr(href)")
        # Hay dos flechas arriba y dos abajo, 4 en total
        if len(flechas_sig_pag) == 4 or self.first_page:
            if self.first_page:
                self.first_page = False
            link_sig_pag = self.crear_sig_url(response.url)
            yield SplashRequest(url=link_sig_pag, callback=self.parse, endpoint='execute', args={'lua_source': self.lua_script_paginar})
        else:
            print("No next page")


    def parse_anuncio(self, response):
        html = response.body.decode(response.encoding)
        match = self.reg_ex_coordenadas.search(html)
        item = response.meta.get('anuncio')
        item['coordenadas'] = match.group()[2:] if match is not None else None
        item['bannos'] = response.css('.icon-bathroom~ .info-value::text').extract()
        item['descripcion'] = response.css('p::text').extract()
        item['telefono'] = response.css('span.phone.icon.icon-call::text')[0].extract()
        yield item

    def crear_sig_url(self, url_viejo):
        reg_ex_pagina= re.compile(r"\.\d+\?")
        match = reg_ex_pagina.search(url_viejo)

        pagina_nueva = int(match.group()[1:-1]) + 1
        inicio_num = match.span()[0]
        fin_num = match.span()[1]
        sig_url = url_viejo[:inicio_num+1] + str(pagina_nueva) + url_viejo[fin_num-1:]
        print(sig_url)

        return sig_url
