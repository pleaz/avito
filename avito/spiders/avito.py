# -*- coding: utf-8 -*-
from avito.items import AvitoItem
import scrapy
import urllib


class AvitSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    query = {'q': 'Камаз 55111'}
    region = 'moskovskaya_oblast'
    start_urls = ['https://www.avito.ru/' + region + '?' + urllib.parse.urlencode(query)]

    def parse(self, response):
        products = response.xpath('//div[contains(@class, "js-catalog_serp")]/div[contains(@class, "js-catalog-item-enum")]')
        for product in products:
            item = AvitoItem()
            item['url'] = response.urljoin(product.xpath('//a[contains(@itemprop, "url")]/@href').extract_first())
            item['name'] = product.xpath('//a[contains(@itemprop, "url")]/text()').extract_first()
            item['price'] = product.xpath('//span[contains(@data-marker, "item-price")]/text()').extract_first()
            yield item

        next = response.xpath('//span[contains(@data-marker, "pagination-button/next")]').extract_first()
        if next:
            parts = urllib.parse.urlparse(response.url)
            query_array = urllib.parse.parse_qs(parts.query)
            if 'p' in query_array:
                query_array['p'][0] = str(int(query_array['p'][0])+1)
            else:
                query_array['p'] = ['2']
            new_query = urllib.parse.urlencode(query_array, True)
            new_parts = parts._replace(query=new_query)
            url = urllib.parse.urlunparse(new_parts)
            yield scrapy.Request(
                url,
                callback=self.parse
            )
