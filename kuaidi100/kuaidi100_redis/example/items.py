# coding=utf-8
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
import scrapy

class ExampleItem(Item):
    movClass = scrapy.Field()#电影分类
    movUrl = scrapy.Field()#电影分类的URL

    mvName = scrapy.Field()
    mvUrl = scrapy.Field()

    downLoadUrl = scrapy.Field()#下载地址
    downLoadName = scrapy.Field()#下载电影的名称
    downimgurl = scrapy.Field()#电影海报图片
    mvdesc = scrapy.Field()#电影的详情介绍
    downdtitle = scrapy.Field()#下载的电影的标题
    pass


class ExampleLoader(ItemLoader):
    default_item_class = ExampleItem
    default_input_processor = MapCompose(lambda s: s.strip())
    default_output_processor = TakeFirst()
    description_out = Join()
