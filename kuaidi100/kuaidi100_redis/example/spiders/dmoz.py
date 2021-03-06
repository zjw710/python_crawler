# coding=utf-8
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import scrapy
from example.items import ExampleItem
import scrapy_redis
class DmozSpider(CrawlSpider):
    """Follow categories and extract links."""
    name = 'dmoz'
    allowed_domains = []
    start_urls = ['http://www.66ys.tv/']

    def parse(self, response):
        i = 0
        for item in response.xpath("/html/body/div[2]/div[2]/ul/li/a"):
            i = i+1
            movClass = item.xpath("text()").extract()
            movUrl = item.xpath("@href").extract_first()
            oneItem = ExampleItem()
            oneItem['movClass'] = movClass
            oneItem['movUrl'] = movUrl
            for j in range(1,2):
                if j==1:
                    mvUrl2 = movUrl+str('index.html')
                else:
                    mvUrl2 = movUrl+str('index_%s.html'%j)
                try:
                    # print("++++++++++"+mvUrl2)
                    # yield oneItem
                    # yield scrapy.Request(url=mvUrl2,callback=lambda response,mvclass=movClass: self.parse_url(response,mvclass))
                    yield scrapy.Request(url=mvUrl2,callback=self.parse_url())
                except Exception as error:
                    print("-------------")
                    print(error)
                    pass
                except RuntimeError as error:
                    print("******************")
                    print(error)
            if i>2:
                break
    # def parse_url(self, response,mvclass):
    def parse_url(self):
        i = 0
        print("++++++++++++++++++++++++")
        yield
        # for sel2 in response.xpath('//div[@class="listBox"]/ul/li'):
        #     i = i+1
        #     imgurl = sel2.xpath("div/a/img/@src").extract()
        #     mvname = sel2.xpath('div/h3/a/text()').extract()#电影名字
        #     mvurl = sel2.xpath("div/h3/a/@href").extract_first()#电影链接
            # oneItem = ExampleItem()
            # oneItem['mvUrl'] = 123456
            # oneItem['mvName'] = 'abcdef'
            # if i>5:
            #     break
            # yield #oneItem
            # yield scrapy.Request(url=mvurl,callback=lambda response,mvsclass=mvclass,img=imgurl,name=mvname,mvUrl=mvurl: self.parse_mor(response,mvsclass,img,name,mvUrl))

    def parse_mor(self, response,mvsclass,img,name,mvUrl):
        for select in response.xpath('//div[@class="contentinfo"]'):
            mvdownloadUrl = select.xpath("div/table/tbody/.//tr/td/a/@href").extract()  # 下载地址,可能是多个
            mvdtilte = select.xpath("div/table/tbody/.//tr/td/a/text()").extract()#下载标签的文本
            mvdesc = select.xpath("div[@id='text']/.//p/text()")#/p[2]/text()
            desc = ''
            for p in mvdesc:
                desc = desc+p.extract().strip()

            # desc= str(desc).replace('\\u3000','  ')
            mvdownloadUrl = ";".join(mvdownloadUrl)
            Item = ExampleItem()
            Item['movClass'] = mvsclass
            Item['downLoadName'] = name
            if str(mvdtilte).strip()=='':
                mvdtilte = "点击下载"
            Item['downdtitle'] = str(mvdtilte)
            Item['downimgurl'] = img
            Item['downLoadUrl'] = mvdownloadUrl
            Item['mvdesc'] = desc
            Item['mvUrl'] = mvUrl
            yield Item
        pass
