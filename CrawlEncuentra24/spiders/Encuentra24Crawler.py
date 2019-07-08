# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class Encuentra24crawlerSpider(CrawlSpider):
    name = 'Encuentra24Crawler'
    allowed_domains = ['encuentra24.com/costa-rica-en/searchresult/real-estate-for-sale#search=f_currency.crc']
    start_urls = ['http://encuentra24.com/costa-rica-en/searchresult/real-estate-for-sale#search=f_currency.crc/']

    rules = (
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = {}

        return item
