import scrapy
from scrapy import Selector
from scrapy_splash import SplashRequest, SplashTextResponse

from ..items import Crawlencuentra24Item

class Ecncuentra24Spider(scrapy.Spider):
    name = 'Encuentra24Spider'
    start_urls = ['https://www.encuentra24.com/costa-rica-en/searchresult/real-estate-for-sale#search=f_currency.crc&regionslug=san-jose-san-jose-capital&page=1']
    BASE_URL = 'https://www.encuentra24.com'

    lua_script = '''
function main(splash, args)
  assert(splash:go(args.url))
  wait_for_element(splash, '.location a', 10)
  btn = splash:select('.location a')
  btn:mouse_click()
  splash:wait(4)
  --wait_for_element(splash, '.place-name div', 10)
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
end
'''

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, endpoint='render.html', args={'wait': 10})

    def parse(self, response):
        anuncios = Crawlencuentra24Item()

        todos_los_anuncions = response.css("article")

        for anuncio in todos_los_anuncions:
            anuncios['titulo'] = anuncio.css("strong::text").extract()
            anuncios['ubicacion'] = anuncio.css(".ann-info-item::text").extract()
            anuncios['precio'] = anuncio.css(".ann-price-2nd div::text").extract()
            anuncios['metrosCuadrados'] = anuncio.css(".icon-area+ .value::text").extract()
            anuncios['habitaciones'] = anuncio.css(".icon-category-home+ .value::text").extract()
            anuncios['descripcion'] = anuncio.css(".ann-box-desc::text").extract()

            link_anuncio = anuncio.css(".ann-box-title::attr(href)").get()

            yield SplashRequest(url=self.BASE_URL + link_anuncio, callback=self.parse_anuncio, endpoint='execute', args={'wait': 1, 'lua_source': self.lua_script})

            yield anuncios

    def parse_anuncio(self, response):
        selector = Selector(text=response.body)
        coordenadas = selector.css('.place-name::text').extract_first()
        print(coordenadas)
