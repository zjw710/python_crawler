#coding=utf-8
#手机号标记查询
##13800138006 ，18122363191 ， 02039999993
import sys
reload(sys)
sys.path.append('..')
from Common.MyDriver import MyDriver
from Common.common import *
import time

sys.setdefaultencoding('utf-8')

class Best114(object):
    def __init__(self):
        self.url = "http://www.114best.com/dh/114.aspx?w="
        self.baseUrl = "http://www.114best.com"
        # self.driver = webdriver.Firefox()
        pass
    def GetBiaoji(self,myDriver,phone_num):
        url = self.url+phone_num
        driver = myDriver.GetUrl(url)
        if not driver:
            LogErrorBest(u"浏览器异常，查询结束")
            return
        try:
            code = 0
            check_num = 1
            tip_img = ""
            while True:
                if check_num>2:#检查2次失败，则退出
                    break
                try:
                    tip_img = driver.find_element_by_xpath('//*[@id="gsName"]/img').get_attribute("src")#测试号码02039999993
                except Exception as e:
                    LogInfoBest(e)
                #如果查不到公司标记，则查个人标记
                if not tip_img:
                    try:
                        tip_img = driver.find_element_by_xpath('//*[@id="tag_Name"]/img').get_attribute("src")#测试号码：15900773083
                    except Exception as e:
                        LogInfoBest(e)
                if not tip_img.strip():#如果为空，则继续查询
                    check_num = check_num+1
                    LogInfoBest("第%s次查询,未查到结果,继续执行查询"%check_num)
                    time.sleep(1)
                    continue
                break

        except Exception as e:
            LogInfoBest(e)
        if not tip_img.strip():
            LogInfoBest("查找不到标记")
            code = 1
        else:
            LogInfoBest("查找到标记:%s"%tip_img)
        # result = {"type":"Best114","code":code,"tip_img":tip_img}
        result = tip_img
        return result

def get_data(best):
    myDriver = MyDriver()
    while True:
        phone_num = raw_input("请输入手机号：")
        if phone_num=='exit':
            return
        result = best.GetBiaoji(myDriver,phone_num)
        LogInfoBest(result)
def LogInfoBest(str):
    log_info("[Best]%s"%str)
def LogErrorBest(str):
    log_error("[Best]%s"%str)
if __name__ == '__main__':
    best = Best114()
    get_data(best)
    # phone_num = "13113140381"
    # best.GetBiaoji(phone_num)


