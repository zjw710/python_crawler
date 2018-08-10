# -*- coding: utf-8 -*-
# -*-coding:gbk-*-
import scrapy
from First.items import FirstItem

class SecondSpider(scrapy.Spider):
    name = 'second'
    allowed_domains = []
    start_urls = ['https://www.lagou.com/']
    cookie = {
        "JSESSIONID":"ABAAABAAAFCAAEG6D560CCADA611A4D5095E984BCE9C199",
        "_ga":"GA1.2.1574432026.1533889022",
        "_gid":"GA1.2.1819997307.1533889022",
        "Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6":"1533889022",
        "user_trace_token":"20180810161704-c3bf5ea5-9c75-11e8-a37b-5254005c3644",
        "LGUID":"20180810161704-c3bf622e-9c75-11e8-a37b-5254005c3644",
        "index_location_city":"%E5%85%A8%E5%9B%BD",
        "TG-TRACK-CODE":"index_navigation",
        "SEARCH_ID":"b22078bb5d20453ba8091bf883db9623",
        "Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6":"1533892624",
        "_gat":"1",
        "LGSID":"20180810171706-26ddacd1-9c7e-11e8-a37b-5254005c3644",
        "PRE_UTM":"",
        "PRE_HOST":"",
        "PRE_SITE":"https%3A%2F%2Fwww.lagou.com%2F",
        "PRE_LAND":"https%3A%2F%2Fwww.lagou.com%2Fzhaopin%2FJava%2F%3FlabelWords%3Dlabel",
        "LGRID":"20180810171706-26ddaf46-9c7e-11e8-a37b-5254005c3644"

    }
    def parse(self, response):
        for item in response.xpath('//*[@id="sidebar"]/div/div[1]/div[2]/dl[1]/dd/a'):
            jobClass = item.xpath('text()').extract()
            jobUrl = item.xpath('@href').extract_first()

            oneItem = FirstItem()
            oneItem['jobClass'] = jobClass
            oneItem['jobUrl'] = jobUrl
            # yield oneItem
            for i in range(5):
                jobUrl2 = jobUrl+str(i+1)
                try:
                    yield scrapy.Request(url=jobUrl2,cookies=self.cookie,callback=self.parse_url)
                except:
                    pass
    def parse_url(self, response):
        for sel2 in response.xpath('//*[@id="s_position_list"]/ul/li'):
            jobName = sel2.xpath('div/div/div/a/h3/text()').extract()
            jobMoney = sel2.xpath('div/div/div/div/span/text()').extract()
            jobNeed = sel2.xpath('div/div/div/div/text()').extract()
            jobCompany = sel2.xpath('div/div/div/a/text()').extract()
            jobType = sel2.xpath('div/div/div/text()').extract()
            jobType = jobType[7].strip()#处理掉换行字符
            jobSpesk = sel2.xpath('div[@class="list_item_bot"]/div/text()').extract()
            jobSpesk = jobSpesk[-1].strip()#处理掉换行字符

            Item = FirstItem()
            Item["jobName"] = jobName
            Item["jobMoney"] = jobMoney
            Item["jobNeed"] = jobNeed
            Item["jobCompany"] = jobCompany
            Item["jobType"] = jobType
            Item["jobSpesk"] = jobSpesk
            yield Item

