#coding=utf-8
#搜狗搜索
#13800138006 ，18122363191 ， 02039999993 ， 17640298760
from selenium import webdriver
from Common.MyDriver import MyDriver
from Common.common import *
import time
import sys
import json
reload(sys)
sys.setdefaultencoding('utf-8')
class Sogo(object):
    def __init__(self):
        self.url = "https://www.sogou.com/web?query="
        pass
    def GetBiaoji(self,myDriver,phone_num):
        url = self.url+phone_num
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
                    info = u"查询%s次查无标记，结束查询"%check_max_num
                    # print(info)
                    LogInfoSogo(info)
                    break
                try:
                    remark = driver.find_element_by_class_name("haoma-tag").text#查询被标记
                except Exception as e:
                    remark = ""
                    LogErrorSogo(e)
                if not remark.strip():
                    info = u"第%s次查询,未查到结果,继续执行查询"%check_num
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
        except Exception as e:
            info = u"查找异常"
            # print(info)
            # print(e)
            LogErrorSogo(info)
            LogErrorSogo(e)
        # result = {"type":"Sogo","code":code,"remark":remark}
        result = remark
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


