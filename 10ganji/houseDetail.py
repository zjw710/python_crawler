#coding=utf-8
#百度手机卫士
#13800138006 ，18122363191 ， 02039999993
import sys
from Common.MyDriver import MyDriver
from Common.common import *
import json
import time
from Common.MyRedis import MyRedis
reload(sys)
sys.setdefaultencoding('utf-8')
class housesDetail(object):
    def __init__(self):
        self.url = "http://gz.ganji.com/wbdetail/ershoufang/36353195153289x.shtml#js-house-agent"
        # self.driver = webdriver.Firefox()
        pass
    def GetPhone(self,myDriver):
        my_redis = MyRedis()

        while(True):
            try:
                url = my_redis.getHouseItemUrl()
                if not url:
                    break
                driver = myDriver.GetUrl(url)
                user_info = driver.find_element_by_class_name("user-info-top").text
                phone = driver.find_element_by_class_name("phone_num").text
                my_redis.addHousePhone(phone,user_info)
                my_log.logger.info("获取到号码：%s %s"%(phone,user_info))
                my_redis.removeHouseItemUrl(url)

                sleep_time = random.randint(1,10)
                time.sleep(sleep_time)
                print("sleep %s秒"%sleep_time)
            except Exception as e:
                my_log.logger.error("查找异常")
                my_log.logger.error(e)
                sleep_time = random.randint(1,5)
                time.sleep(sleep_time)
                print("sleep %s秒"%sleep_time)
                break
        # result = remark

def get_data(ganji):
    myDriver = MyDriver()
    result = ganji.GetPhone(myDriver)

if __name__ == '__main__':
    housesDetail = housesDetail()
    get_data(housesDetail)
    # phone_num = "13113140381"
    # baidu.GetBiaoji(phone_num)


