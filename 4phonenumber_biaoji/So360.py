#coding=utf-8
#360搜索
#13800138006 ，18122363191 ， 02039999993 ， 17640298760
from selenium import webdriver
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class So360(object):
    def __init__(self):
        self.url = "https://www.so.com/s?ie=utf-8&fr=none&src=360sou_newhome&q="
        self.driver = webdriver.Firefox()
        pass
    def GetBiaoji(self,phone_num):
        driver = self.driver
        url = self.url+phone_num
        try:
            driver.get(url)
        except Exception as e:
            print("浏览器异常,重新打开浏览器")
            print(e)
            try:
                self.driver = webdriver.Firefox()
                driver = self.driver
                driver.get(url)
            except Exception as e:
                print("重新打开浏览器异常，不再尝试")
                print(e)
                return
        try:
            print("等待1s...")
            time.sleep(1)

            check_num = 1#检查次数
            check_max_num = 2
            while True:
                if check_num>check_max_num:
                    remark = ""
                    print("查询%s次查无标记，结束查询"%check_max_num)
                    break
                try:
                    remark = driver.find_element_by_class_name("mohe-ph-mark").text#查询被标记
                except Exception as e:
                    remark = ""
                    print(e)
                try:
                    com_img = driver.find_element_by_class_name("mh-hy-img").get_attribute("src")#查询企业标记
                except Exception as e:
                    com_img = ""
                    print(e)
                try:
                    tip_img = driver.find_element_by_xpath('//*[@class="mohe-tips"]/strong/img').get_attribute("src")
                except Exception as e:
                    tip_img = ""
                    print(e)
                if not remark.strip() and not com_img.strip() and not tip_img.strip():
                    print("第%s次查询,未查到结果,继续执行查询"%check_num)
                    check_num = check_num+1
                    time.sleep(1)
                    continue
                #结束循环
                break
            if not remark.strip() and not com_img.strip() and not tip_img.strip():
                print("查不到标记")
            else:
                print("查找到被标记remark:%s"%(remark))
                print("查找到公司标记com_img:%s"%(com_img))
                print("查找到被标记tip_img:%s"%(tip_img))
        except Exception as e:
            print("查找异常")
            print(e)
def get_data(so360):
    while True:
        phone_num = raw_input("请输入手机号：")
        if phone_num=='exit':
            return
        so360.GetBiaoji(phone_num)

if __name__ == '__main__':
    so360 = So360()
    get_data(so360)
    # phone_num = "13113140381"
    # baidu.GetBiaoji(phone_num)


