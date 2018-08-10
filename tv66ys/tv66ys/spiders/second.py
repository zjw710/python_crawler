# -*- coding: utf-8 -*-
import scrapy


class SecondSpider(scrapy.Spider):
    name = 'second'
    allowed_domains = []
    start_urls = ['http://www.66ys.tv/']

    def parse(self, response):
        pass
