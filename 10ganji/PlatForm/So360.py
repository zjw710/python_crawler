#coding=utf-8
#360搜索
#13800138006 ，18122363191 ， 02039999993 ， 17640298760
import sys
sys.path.append('..')
from Common.MyDriver import MyDriver
from Common.common import *
from selenium import webdriver
import time
reload(sys)
import json
sys.setdefaultencoding('utf-8')
class So360(object):
    def __init__(self):
        self.url = "https://www.so.com/s?ie=utf-8&fr=none&src=360sou_newhome&q="
        pass
    def GetBiaoji(self,myDriver,phone_num):
        phone_num = str(phone_num)
        url = self.url+str(phone_num)
        driver = myDriver.GetUrl(url)
        if not driver:
            LogErrorSo360(u"浏览器异常，查询结束")
            return
        try:
            #初始化数据
            code = 0
            remark = com_img = tip_img =""
            info = u"开始查询..."
            # print(info)
            LogInfoSo360(info)
            # time.sleep(1)
            check_num = 1#检查次数
            check_max_num = 2
            while True:
                if check_num>check_max_num:
                    remark = ""
                    info = u"查询%s次查无标记，结束查询"%str(check_max_num)
                    # print(info)
                    LogInfoSo360(info)
                    break
                try:
                    remark = driver.find_element_by_class_name("mohe-ph-mark").text#查询被标记
                except Exception as e:
                    remark = ""
                    LogInfoSo360(e)
                try:
                    com_img = driver.find_element_by_class_name("mh-hy-img").get_attribute("src")#查询企业标记
                    com_img = com_img.replace('+','%2B')
                except Exception as e:
                    com_img = ""
                    LogInfoSo360(e)
                try:
                    tip_img = driver.find_element_by_xpath('//*[@class="mohe-tips"]/strong/img').get_attribute("src")
                    tip_img = tip_img.replace('+','%2B')
                except Exception as e:
                    tip_img = ""
                    LogInfoSo360(e)
                if not remark.strip() and not com_img.strip() and not tip_img.strip():
                    info = u"第%s次查询,未查到结果,继续执行查询"%str(check_num)
                    # print(info)
                    LogInfoSo360(info)
                    check_num = check_num+1
                    time.sleep(1)
                    continue
                #结束循环
                break
            if not remark.strip() and not com_img.strip() and not tip_img.strip():
                info = u"查不到标记"
                # print(info)
                LogInfoSo360(info)
            else:
                code = 1
                info = "查找到被标记remark:%s"%(remark)
                LogInfoSo360(info)
                info = "查找到公司标记com_img:%s"%(com_img)
                LogInfoSo360(info)
                info = "查找到被标记tip_img:%s"%(tip_img)
                LogInfoSo360(info)
            myDriver.ScreenShot(str(phone_num)+"so360")
        except Exception as e:
            myDriver.ScreenShot(str(phone_num)+"so360","error")
            info = u"查找异常"
            LogErrorSo360(info)
            LogErrorSo360(e)
        # result = {"type":"So360","code":code,"remark":remark,"com_img":com_img,"tip_img":tip_img}
        result = remark+","+com_img+","+tip_img
        result = [{"p":"360mark","m":remark},{"p":"360com","m":com_img},{"p":"360bus","m":tip_img}]
        result = json.dumps(result)
        return result
def get_data(so360):
    myDriver = MyDriver()
    while True:
        phone_num = raw_input("请输入手机号：")
        if phone_num=='exit':
            return
        result = so360.GetBiaoji(myDriver,phone_num)
        LogInfoSo360(result)
def LogInfoSo360(str):
    log_info("[So360]%s"%str)
def LogErrorSo360(str):
    log_error("[So360]%s"%str)
if __name__ == '__main__':
    so360 = So360()
    get_data(so360)
    # phone_num = "13113140381"
    # baidu.GetBiaoji(phone_num)


