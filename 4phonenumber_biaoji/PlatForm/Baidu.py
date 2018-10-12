#coding=utf-8
#百度手机卫士
#13800138006 ，18122363191 ， 02039999993
from selenium import webdriver
import sys
sys.path.append('..')
from Common.MyDriver import MyDriver
from Common.common import *
import json
import time

reload(sys)
sys.setdefaultencoding('utf-8')
class Baidu(object):
    def __init__(self):
        self.url = "https://haoma.baidu.com/query"
        # self.driver = webdriver.Firefox()
        pass
    def GetBiaoji(self,myDriver,phone_num):
        url = self.url
        driver = myDriver.GetUrl(url)
        if not driver:
            LogErrorBaidu(u"浏览器异常，查询结束")
            return
        try:
            code = 0
            remark = ""
            LogInfoBaidu("等待0.5s...")
            time.sleep(0.5)
            search_input = driver.find_element_by_id("id_phone")
            search_input.send_keys(phone_num)
            submit_btn = driver.find_element_by_xpath('//*[@class="submit"]')
            submit_btn.click()
            time.sleep(0.1)#等待1秒
            submit_btn.click()
            check_num = 0#检查次数
            while True:
                if check_num>3:
                    remark = ""
                    code = 0
                    break
                try:
                    remark = driver.find_element_by_xpath('//*[@class="category"]/h2').text
                except Exception as e:
                    check_num = check_num+1
                    LogInfoBaidu("第%s次查询,未查到结果,继续执行查询"%check_num)
                    LogInfoBaidu(e)
                    time.sleep(1)
                    continue

                num_remark = ""
                try:
                    num_remark = driver.find_element_by_xpath('//*[@class="category"]/span[1]').text
                except Exception as e:
                    LogInfoBaidu("未获得标记人数")
                    LogInfoBaidu(e)
                #结束循环
                break
            LogInfoBaidu("查找到的标记remark:%s %s"%(remark,num_remark))
            code=1
        except Exception as e:
            LogErrorBaidu("查找异常")
            LogErrorBaidu(e)
        # result = remark
        result = [{"p":"baidu","m":remark}]
        result = json.dumps(result)
        return result
def get_data(baidu):
    myDriver = MyDriver()
    while True:
        phone_num = raw_input("请输入手机号：")
        if phone_num=='exit':
            return
        result = baidu.GetBiaoji(myDriver,phone_num)
        LogInfoBaidu(result)
#写日志
def LogInfoBaidu(str):
    log_info("[Baidu]%s"%str)
def LogErrorBaidu(str):
    log_error("[Baidu]%s"%str)
if __name__ == '__main__':
    baidu = Baidu()
    get_data(baidu)
    # phone_num = "13113140381"
    # baidu.GetBiaoji(phone_num)


