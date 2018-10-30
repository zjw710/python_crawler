#coding=utf-8
#百度号码
#13800138006 ，18122363191 ， 02039999993
from selenium import webdriver
import sys
reload(sys)
sys.path.append('..')
from Common.MyDriver import MyDriver
from Common.common import *
import time
import json
sys.setdefaultencoding('utf-8')
class Baiduhaoma(object):
    def __init__(self):
        self.url = "https://haoma.baidu.com/phoneSearch?position=&request_page=1&search="
        pass
    def GetBiaoji(self,myDriver,phone_num):
        phone_num = str(phone_num)
        url = self.url+str(phone_num)
        driver = myDriver.GetUrl(url)
        remark = ""
        if not driver:
            LogErrorBaidu(u"浏览器异常，查询结束")
            return
        try:
            check_num = 0#检查次数
            while True:
                if check_num>1:
                    remark = ""
                    break
                try:
                    remark1 = driver.find_element_by_xpath('//*[@class="report_text"]/div').text#测试号码：15900773083
                except Exception as e:
                    LogErrorBaidu(e)
                    remark1 = ""
                try:
                    remark2 = driver.find_element_by_xpath('//*[@class="item_line1"]/div').text#测试号码：18984257093
                except Exception as e:
                    LogErrorBaidu(e)
                    remark2 = ""
                #如果两个都查不到，则查多一次
                if not remark1 and not remark2:
                    check_num = check_num+1
                    LogInfoBaidu("第%s次查询,未查到结果,继续执行查询"%str(check_num))
                    time.sleep(1)
                    continue
                remark = remark1+remark2
                #结束循环
                break
            myDriver.ScreenShot(str(phone_num)+"baiduhaoma")
            LogInfoBaidu("查找到的标记remark:%s"%(remark))
        except Exception as e:
            myDriver.ScreenShot(str(phone_num)+"baiduhaoma","error")
            LogErrorBaidu("查找异常")
            LogErrorBaidu(e)
        # result = remark
        result = [{"p":"baiduhaoma","m":remark}]
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
    baiduhaoma = Baiduhaoma()
    get_data(baiduhaoma)
    # phone_num = "13113140381"
    # baidu.GetBiaoji(phone_num)


