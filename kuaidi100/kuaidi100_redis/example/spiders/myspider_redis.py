from scrapy_redis.spiders import RedisSpider


class MySpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'myspider_redis'
    redis_key = 'myspider:start_urls'#668976000011
    #http://m.kuaidi100.com/result.jsp?com=tiantian&nu=668976000012
    #http://m.kuaidi100.com/result.jsp?com=tiantian&nu=668976000990

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(MySpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        num = response.xpath('//*[@id="queryInput"]/@value').extract()
        result_list = response.xpath('//*[@id="result"]').extract()
        mobile = response.xpath('//*[@id="result"]/li[2]/div[3]/a[1]/text()').extract()
        return {
            'name': response.css('title::text').extract_first(),
            'url': response.url,
            'num':num,
            'result_list':result_list,
            'mobile':mobile,
        }
