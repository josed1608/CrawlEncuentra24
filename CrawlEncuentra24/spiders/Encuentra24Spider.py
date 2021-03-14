import scrapy
from scrapy import Request
from scrapy_splash import SplashRequest
import re
import time
import os
import logging
import CrawlEncuentra24.constants as constants

from ..items import Crawlencuentra24Item

class Ecncuentra24Spider(scrapy.Spider):
    name = 'Encuentra24Spider'
    # Los links contienen los filtros de localización y de tipo de propiedad
    start_urls = [
        # link alquileres
        'https://www.encuentra24.com/costa-rica-es/bienes-raices-alquiler-apartamentos.1?regionslug=san-jose-provincia-san-jose-capital,san-jose-provincia-alajuelita,san-jose-provincia-aserri,san-jose-provincia-curridabat,san-jose-provincia-desamparados,san-jose-provincia-escazu,san-jose-provincia-goicoechea,san-jose-provincia-montes-de-oca,san-jose-provincia-moravia,san-jose-provincia-mora,san-jose-provincia-santa-ana,san-jose-provincia-tibas,san-jose-provincia-vazquez-de-coronado,alajuela-provincia-alajuela,alajuela-provincia-atenas,alajuela-provincia-poas,cartago-provincia-cartago,cartago-provincia-san-rafael,cartago-provincia-paraiso,cartago-provincia-pacayas,cartago-provincia-tres-rios,cartago-provincia-tejar,heredia-provincia-heredia,heredia-provincia-barva,heredia-provincia-santo-domingo,heredia-provincia-santa-barbara,heredia-provincia-san-rafael,heredia-provincia-san-isidro,guanacaste-provincia-belen,heredia-provincia-flores,heredia-provincia-san-pablo&q=withcat.bienes-raices-alquiler-apartamentos,bienes-raices-alquiler-casas,bienes-raices-alquiler-comercios,bienes-raices-alquiler-apartamentos-amueblados,bienes-raices-alquiler-alquiler-de-oficinas,bienes-raices-alquiler-cuartos,bienes-raices-alquiler-negocios,bienes-raices-alquiler-casas-de-playa,bienes-raices-alquiler-casas-en-el-interior',
        #link anuncios
        'https://www.encuentra24.com/costa-rica-es/bienes-raices-venta-de-propiedades-casas.1?regionslug=san-jose-provincia-san-jose-capital,san-jose-provincia-alajuelita,san-jose-provincia-aserri,san-jose-provincia-curridabat,san-jose-provincia-desamparados,san-jose-provincia-escazu,san-jose-provincia-goicoechea,san-jose-provincia-montes-de-oca,san-jose-provincia-moravia,san-jose-provincia-mora,san-jose-provincia-santa-ana,san-jose-provincia-tibas,san-jose-provincia-vazquez-de-coronado,alajuela-provincia-alajuela,alajuela-provincia-atenas,alajuela-provincia-poas,cartago-provincia-cartago,cartago-provincia-san-rafael,cartago-provincia-paraiso,cartago-provincia-pacayas,cartago-provincia-tres-rios,cartago-provincia-tejar,heredia-provincia-heredia,heredia-provincia-barva,heredia-provincia-santo-domingo,heredia-provincia-santa-barbara,heredia-provincia-san-rafael,heredia-provincia-san-isidro,guanacaste-provincia-belen,heredia-provincia-flores,heredia-provincia-san-pablo&q=withcat.bienes-raices-venta-de-propiedades-casas,bienes-raices-venta-de-propiedades-apartamentos,bienes-raices-venta-de-propiedades-lotes-y-terrenos,bienes-raices-venta-de-propiedades-comercios,bienes-raices-venta-de-propiedades-fincas,bienes-raices-venta-de-propiedades-edificios,bienes-raices-venta-de-propiedades-oficinas,bienes-raices-venta-de-propiedades-negocios,bienes-raices-venta-de-propiedades-casas-y-terrenos-de-playas'
    ]
    BASE_URL = 'https://www.encuentra24.com'

    reg_ex_coordenadas = re.compile(r"q=-?\d+\.\d+,-?\d+\.\d+")
    reg_ex_rebaja = re.compile(r"\d+%")
    reg_ex_pagina = re.compile(r"\.\d+\?")

    id_auto_incrementado = 0
    first_page_venta = True
    first_page_alquiler = True

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, endpoint='execute', args={'lua_source': constants.lua_script_paginar}, meta={'pagina': 1})

    def parse(self, response, **kwargs):
        todos_los_anuncions = response.css('article')
        link_primer_anuncio = todos_los_anuncions[0].css('.ann-box-title::attr(href)').get()
        tipo_de_anuncio = 'alquiler' if '/costa-rica-es/bienes-raices-alquiler' in link_primer_anuncio else 'venta'

        for anuncio in todos_los_anuncions:
            # Para no sobrecargar a Encuentra24
            time.sleep(1)

            item_anuncio = Crawlencuentra24Item()
            link_anuncio = self.BASE_URL + anuncio.css('.ann-box-title::attr(href)').get()
            item_anuncio['pagina'] = response.meta.get('pagina')
            item_anuncio['link'] = link_anuncio
            item_anuncio['tipo_de_anuncio'] = tipo_de_anuncio

            yield Request(url=link_anuncio, callback=self.parse_anuncio, meta={'anuncio':  item_anuncio})

        flechas_sig_pag = response.css('nav li.arrow a::attr(href)')
        # Hay dos flechas arriba y dos abajo, 4 en total, excepto en la primera y última página que hay solo dos
        if len(flechas_sig_pag) == 4 \
                or (tipo_de_anuncio == 'venta' and self.first_page_venta)\
                or (tipo_de_anuncio == 'alquiler' and self.first_page_alquiler):

            if tipo_de_anuncio == 'venta' and self.first_page_venta:
                self.first_page_venta = False
            elif tipo_de_anuncio == 'alquiler' and self.first_page_alquiler:
                self.first_page_alquiler = False

            (link_sig_pag, sig_pag) = self.crear_sig_url(response.url)
            self.cooldown_splash(sig_pag)
            yield SplashRequest(url=link_sig_pag, callback=self.parse, endpoint='execute', args={'lua_source': constants.lua_script_paginar}, meta={'pagina': sig_pag})
        else:
            logging.info("No next page")


    def parse_anuncio(self, response):

        item = response.meta.get('anuncio')

        item['titulo'] = response.css('.product-title::text').extract()

        precio = response.css('.offer-price::text').extract()[0].split('\xa0')[0][1:]
        columna_precio = 'precio_dolares' if precio[0] == '$' else 'precio_colones'
        item[columna_precio] = precio

        item['metros_cuadrados'] = response.css('.icon-area~ .info-value::text').extract()

        item['habitaciones'] = response.css('.icon-category-home~ .info-value::text').extract()

        html = response.body.decode(response.encoding)
        match = self.reg_ex_coordenadas.search(html)
        item['coordenadas'] = match.group()[2:] if match is not None else None

        item['bannos'] = response.css('.icon-bathroom~ .info-value::text').extract()

        item['descripcion'] = response.css('p::text').extract()

        item['telefono_publicador'] = response.css('span.phone.icon.icon-call::text')[0].extract()

        self.obtener_canton_y_distrito(item, response)

        item['tipo_de_uso'] = response.css('.breadcrumb li:nth-child(4) a::text').extract()

        rebaja = response.css('.ann-price-reduced::text').extract()

        if len(rebaja) != 0:
            match = self.reg_ex_rebaja.search(rebaja[0])
            item['porcentaje_rebaja'] = match.group() if match is not None else None

        item['fecha_de_publicacion'] = response.css('.ad-info li:nth-child(2) .info-value::text').extract()[0]

        # ID is extracted as 'ID: 21312321', so we need to split it in the white-space
        item['id_encuentra24'] = response.css('.ad-id::text').extract()[0].split(' ')[1]

        item['id_autogenerado'] = self.id_auto_incrementado
        self.id_auto_incrementado += 1

        item['parqueos'] = response.css('.icon-category-cars~ .info-value::text').extract()

        item['nombre_publicador'] = response.css('.user-name::text').extract()[0]

        datos_publicador = response.css('.text-attr::text').extract()
        item['datos_publicador'] = datos_publicador[:len(datos_publicador)//2]

        yield item

    def crear_sig_url(self, url_viejo):
        match = self.reg_ex_pagina.search(url_viejo)

        pagina_nueva = int(match.group()[1:-1]) + 1
        inicio_num = match.span()[0]
        fin_num = match.span()[1]
        sig_url = url_viejo[:inicio_num+1] + str(pagina_nueva) + url_viejo[fin_num-1:]

        return (sig_url, pagina_nueva)

    def obtener_canton_y_distrito(self, item, response):
        provincia = response.css('.breadcrumb li:nth-child(5) a::text').extract()
        canton = response.css('.breadcrumb li:nth-child(6) a::text').extract()
        distrito = response.css('.breadcrumb li:nth-child(7) a::text').extract()

        # Para estos 3 cantones Encuentra24 no da un filtro, pero sí para uno de los distritos por cantón,
        # por lo que hay que hacer el ajuste manual
        if (canton == 'San Rafael' and provincia == 'Cartago'):
            distrito = canton
            canton = 'Oreamuno'
        elif (canton == 'Pacayas'):
            distrito = canton
            canton = 'Alvarado'
        elif(canton == 'Tejar'):
            distrito = canton
            canton = 'El Guarco'

        item['provincia'] = provincia
        item['canton'] = canton
        item['distrito'] = distrito

    #Cada 30 páginas reincia la imagen de docker para evitar sobrecargarla
    def cooldown_splash(self, numero_pagina):
        if numero_pagina % 30 == 0:
            logging.info('Restarting docker image to cooldown. Page number ' + str(numero_pagina))
            os.system(constants.stop_docker_command)
            logging.info('Stopped docker image, restarting...')
            os.system(constants.start_docker_command)
            time.sleep(30)
            logging.info('Finished restarting docker image')
