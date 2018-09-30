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
sys.setdefaultencoding('utf-8')
class Baiduwap(object):
    def __init__(self):
        self.url = "http://wap.baidu.com/s?word="
        pass
    def GetBiaoji(self,myDriver,phone_num):
        url = self.url+phone_num
        platform = remark = ""

        # if not driver:
        #     LogErrorBaidu(u"浏览器异常，查询结束")
        #     return
        try:
            check_num = 0#检查次数
            while True:
                if check_num>2:
                    remark = ""
                    break
                #由于百度有时候需要查多几次才出现电话邦，因此此处通过循环查询的方式
                driver = myDriver.GetUrl(url)
                try:
                    remark = driver.find_element_by_xpath('//*[@class="wa-fraudphone-font"]').text#测试号码：15651656722
                except Exception as e:
                    LogErrorBaidu(e)
                    remark = ""
                # if not remark:
                #     try:
                #         remark = driver.find_element_by_class_name('c-gap-right c-text-box c-text-box-red').text#测试号码：13800138006
                #     except Exception as e:
                #         LogErrorBaidu(e)
                #         remark = ""
                try:
                    ori_platform = driver.find_element_by_class_name("c-color-gray").text#测试号码：18984257093
                    m_index = ori_platform.find("标记为")
                    # print(platform)
                    if ori_platform.find(u"百度手机卫士")>0:#测试号码：13800138006
                        platform = "百度手机卫士"
                    elif ori_platform.find(u"电话邦")>0:#测试号码：13256391586
                        platform = "电话邦"
                    if m_index>0 and remark=="":
                        remark1 = ori_platform[m_index+3:]
                        remark += remark1
                except Exception as e:
                    my_log.logger.error(e)
                    platform = ""
                #如果两个都查不到，则查多一次
                if not remark:
                    check_num = check_num+1
                    LogInfoBaidu("第%s次查询,未查到结果,继续执行查询"%check_num)
                    time.sleep(1)
                    continue
                #结束循环
                break
            my_log.logger.info("查找到的标记remark:%s 平台:%s"%(remark,platform))
        except Exception as e:
            my_log.logger.error("查找异常")
            my_log.logger.error(e)
        result = remark+"-"+platform
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
    baiduwap = Baiduwap()
    get_data(baiduwap)
    # phone_num = "13113140381"
    # baidu.GetBiaoji(phone_num)


