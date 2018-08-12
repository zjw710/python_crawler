# -*- coding: utf-8 -*-
import scrapy
from tv66ys.items import Tv66YsItem

class SecondSpider(scrapy.Spider):
    name = 'second'
    allowed_domains = []
    start_urls = ['http://www.66ys.tv/']

    def parse(self, response):
        for item in response.xpath("/html/body/div[2]/div[2]/ul/li"):
            movClass = item.xpath("text()").extract()
            movUrl = item.xpath("@href").extract_first()
            oneItem = Tv66YsItem()
            oneItem['movClass'] = movClass
            oneItem['movUrl'] = movUrl
            for i in range(2):
                mvUrl2 = movUrl+str('index_%s.html'%i)
                try:
                    yield scrapy.Request(url=mvUrl2,callback=lambda response,mvclass=movClass: self.parse_url(response,mvclass))
                except:
                    pass
    def parse_url(self, response,mvclass):
        for sel2 in response.xpath('//div[@class="listBox"]/ul/li'):
            imgurl = sel2.xpath("div/a/img/@src").extract()
            mvname = sel2.xpath('div/h3/a/text()').extract()#电影名字
            mvurl = sel2.xpath("div/h3/a/@href").extract_first()#电影链接
            yield scrapy.Request(url=mvurl,callback=lambda response,mvsclass=mvclass,img=imgurl,name=mvname: self.parse_mor(response,mvsclass,img,name))
        pass
    def parse_mor(self, response,mvsclass,img,name):
        for select in response.xpath('//div[@class="contentinfo"]'):
        pass
