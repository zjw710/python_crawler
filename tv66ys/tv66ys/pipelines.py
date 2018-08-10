# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from twisted.enterprise import adbapi
import pymysql
from tv66ys import settings
from scrapy import log

class Tv66YsPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True
        )
        self.cursor = self.connect.cursor()
    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """select * from mybt where downLoadName = %s""",
                item['downLoadName']
            )
        except Exception as error:
            log(error)
        return item
