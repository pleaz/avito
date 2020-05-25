# -*- coding: utf-8 -*-
import scrapy


class AvitSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['https://avito.ru']
    start_urls = ['https://avito.ru/']

    def parse(self, response):
        pass
