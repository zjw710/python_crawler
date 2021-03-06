#coding=utf-8
#搜狗搜索
#13800138006 ，18122363191 ， 02039999993 ， 17640298760
from selenium import webdriver

import time
import sys
sys.path.append('..')
from Common.MyDriver import MyDriver
from Common.common import *
import json
reload(sys)
import json
sys.setdefaultencoding('utf-8')
class Sogo(object):
    def __init__(self):
        self.url = "https://www.sogou.com/web?query="
        pass
    def GetBiaoji(self,myDriver,phone_num):
        phone_num = str(phone_num)
        url = self.url+str(phone_num)
        driver = myDriver.GetUrl(url)
        if not driver:
            LogErrorSogo(u"浏览器异常，查询结束")
            return
        try:
            #初始化数据
            code = 0#code为0表示查不到信息，为1表示查找到标记
            remark = ""
            info = u"开始查询..."
            # print(info)
            LogInfoSogo(info)
            # time.sleep(1)

            check_num = 1#检查次数
            check_max_num = 2
            while True:
                if check_num>check_max_num:
                    remark = ""
                    haoma_link = ""
                    info = u"查询%s次查无标记，结束查询"%str(check_max_num)
                    # print(info)
                    LogInfoSogo(info)
                    break
                try:
                    remark = driver.find_element_by_class_name("haoma-tag").text#查询被标记
                except Exception as e:
                    remark = ""
                    LogErrorSogo(e)
                try:
                    haoma_link = driver.find_element_by_class_name("haoma-link").text#判断是否是 搜狗号码通
                    print(haoma_link)
                except Exception as e:
                    haoma_link = ""
                    LogErrorSogo(e)
                if haoma_link.strip().decode('utf-8') == "搜狗号码通".decode('utf-8'):
                    haoma_link = "sogohaoma"
                if not remark.strip():
                    info = u"第%s次查询,未查到结果,继续执行查询"%str(check_num)
                    # print(info)
                    LogInfoSogo(info)
                    check_num = check_num+1
                    time.sleep(1)
                    continue
                #结束循环
                break
            if not remark.strip():
                info = u"查不到标记"
                # print(info)
                LogInfoSogo(info)
            else:
                info = u"查找到被标记remark:%s"%(remark)
                # print(info)
                code = 1
                LogInfoSogo(info)
            myDriver.ScreenShot(str(phone_num)+"sogo")
        except Exception as e:
            myDriver.ScreenShot(str(phone_num)+"sogo","error")
            info = u"查找异常"
            # print(info)
            # print(e)
            LogErrorSogo(info)
            LogErrorSogo(e)
        # result = {"type":"Sogo","code":code,"remark":remark}
        # result = remark
        if not haoma_link.strip():
            result = [{"p":"sogo","m":remark}]
        else:
            result = [{"p":"sogo","m":remark},{"p":haoma_link,"m":remark}]
        result = json.dumps(result)
        return result
def get_data(sogo):
    myDriver = MyDriver()
    while True:
        phone_num = raw_input("请输入手机号：")
        if phone_num=='exit':
            return
        result = sogo.GetBiaoji(myDriver,phone_num)
        LogInfoSogo(result)
def LogInfoSogo(str):
    log_info("[Sogo]%s"%str)
def LogErrorSogo(str):
    log_error("[Sogo]%s"%str)
if __name__ == '__main__':
    sogo = Sogo()
    get_data(sogo)


