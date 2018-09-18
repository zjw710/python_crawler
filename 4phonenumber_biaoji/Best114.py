#coding=utf-8
#手机号标记查询
##13800138006 ，18122363191 ， 02039999993
from selenium import webdriver
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class Best114(object):
    def __init__(self):
        self.url = "http://www.114best.com/dh/114.aspx?w="
        self.baseUrl = "http://www.114best.com"
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
            time.sleep(1)
            # search_input = driver.find_element_by_id("w")
            # search_input.clear()
            # search_input.send_keys(phone_num)
            #
            # search_btn = driver.find_element_by_id("query")
            # search_btn.click()
            check_num = 1
            tag_url = ""
            while True:
                if check_num>2:#检查2次失败，则退出
                    break
                try:
                    tag_url = driver.find_element_by_xpath('//*[@id="gsName"]/img').get_attribute("src")
                except Exception as e:
                    print(e)
                try:
                    tag_url = driver.find_element_by_xpath('//*[@id="tag_Name"]/img').get_attribute("src")
                except Exception as e:
                    print(e)
                if not tag_url.strip():#如果为空，则继续查询
                    time.sleep(1)
                    check_num = check_num+1
                    print("第%s次查询,未查到结果,继续执行查询"%check_num)
                    continue
                break

        except Exception as e:
            tag_url = "无标记"
            print(e)
        if not tag_url.strip():
            print("查找不到标记")
        else:
            print("查找到标记:%s"%tag_url)
def get_data(best):
    while True:
        phone_num = raw_input("请输入手机号：")
        if phone_num=='exit':
            return
        best.GetBiaoji(phone_num)
if __name__ == '__main__':
    best = Best114()
    get_data(best)
    # phone_num = "13113140381"
    # best.GetBiaoji(phone_num)


