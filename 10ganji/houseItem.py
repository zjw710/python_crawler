#coding=utf-8
'''
采集列表页面
'''
import sys
from Common.MyDriver import MyDriver
from Common.common import *
import json
import time
from Common.MyRedis import MyRedis
reload(sys)
sys.setdefaultencoding('utf-8')
class housesItem(object):
    def __init__(self):
        self.url = "http://gz.ganji.com/wblist/ershoufang/pn%s"
        # self.driver = webdriver.Firefox()
        pass
    def GetPageUrl(self,myDriver):
        my_redis = MyRedis()
        url = self.url

        try:
            for page in range(1,71):
                page_url = url%page
                if my_redis.isExistHousePageUrl(page_url):
                    my_log.logger.info("页面已采集：%s"%page_url)
                    continue
                my_log.logger.info(page_url)
                # continue
                driver = myDriver.GetUrl(page_url)

                my_redis.addHousePageUrl(page_url)#把采集过的页面放在redis中
                print("第%s页,url%s"%(page,page_url))

                items = driver.find_elements_by_xpath('//*[@class="dd-item title"]/a')
                # print(type(items))
                # print(items)

                #把采集的页面加入到redis中
                for item in items:
                    houses_url = item.get_attribute('href')
                    my_redis.addHouseItemUrl(houses_url)
                # time.sleep(2)
                # continue

                sleep_time = random.randint(3,8)
                time.sleep(sleep_time)
                print("sleep %s秒"%sleep_time)
            # print(items)
        except Exception as e:
            my_log.logger.error("查找异常")
            my_log.logger.error(e)
        # result = remark

def get_data(ganji):
    myDriver = MyDriver()
    result = ganji.GetPageUrl(myDriver)

if __name__ == '__main__':
    housesItem = housesItem()
    get_data(housesItem)
    # phone_num = "13113140381"
    # baidu.GetBiaoji(phone_num)


