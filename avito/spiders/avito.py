# -*- coding: utf-8 -*-
from avito.items import AvitoItem
import scrapy
import urllib


class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    query = {'q': 'Камаз 6520'}
    region = 'moskovskaya_oblast'
    category = 'gruzoviki_i_spetstehnika'
    start_urls = ['https://www.avito.ru/' + region + '/' + category + '?' + urllib.parse.urlencode(query)] # стартовый url

    def parse(self, response):
        products = response.xpath('//div[contains(@class, "js-catalog_serp")]/div[contains(@class, "js-catalog-item-enum")]') # ищем карточку товара
        for product in products:
            item = AvitoItem()
            item['url'] = response.urljoin(product.xpath('.//a[contains(@itemprop, "url")]/@href').extract_first()) # вытаскиваем url из карточки товара
            item['name'] = product.xpath('.//a[contains(@itemprop, "url")]/text()').extract_first() # вытаскиваем название из карточки товара
            item['price'] = product.xpath('.//span[contains(@data-marker, "item-price")]/text()').extract_first().strip().replace("₽","").replace(" ","") # вытаскиваем цену из карточки товара
            yield item # сохраняем

        next = response.xpath('//span[contains(@data-marker, "pagination-button/next")]').extract_first() # ищем наличие след стр
        if next:
            parts = urllib.parse.urlparse(response.url)
            query_array = urllib.parse.parse_qs(parts.query)
            if 'p' in query_array:
                query_array['p'][0] = str(int(query_array['p'][0])+1) # если стр не первая то переход на +1
            else:
                query_array['p'] = ['2'] # если стр первая то переход на 2
            new_query = urllib.parse.urlencode(query_array, True)
            new_parts = parts._replace(query=new_query)
            url = urllib.parse.urlunparse(new_parts) # тут собирается ссылки на след стр.
            yield scrapy.Request(
                url,
                callback=self.parse # рекурсия на след стр
            )
