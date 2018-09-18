#coding=utf-8
#百度手机卫士
#13800138006 ，18122363191 ， 02039999993
from selenium import webdriver
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class Baidu(object):
    def __init__(self):
        self.url = "https://haoma.baidu.com/query"
        self.driver = webdriver.Firefox()
        pass
    def GetBiaoji(self,phone_num):
        driver = self.driver
        try:
            driver.get(self.url)
        except Exception as e:
            print("浏览器异常,重新打开浏览器")
            print(e)
            try:
                self.driver = webdriver.Firefox()
                driver = self.driver
                driver.get(self.url)
            except Exception as e:
                print("重新打开浏览器异常，不再尝试")
                print(e)
                return
        try:
            print("等待1s...")
            time.sleep(1)
            search_input = driver.find_element_by_id("id_phone")
            search_input.send_keys(phone_num)
            submit_btn = driver.find_element_by_xpath('//*[@class="submit"]')
            submit_btn.click()
            time.sleep(0.1)#等待1秒
            submit_btn.click()
            check_num = 0#检查次数
            while True:
                if check_num>5:
                    remark = ""
                    break
                try:
                    remark = driver.find_element_by_xpath('//*[@class="category"]/h2').text
                except Exception as e:
                    check_num = check_num+1
                    print("第%s次查询,未查到结果,继续执行查询"%check_num)
                    print(e)
                    time.sleep(1)
                    continue

                num_remark = ""
                try:
                    num_remark = driver.find_element_by_xpath('//*[@class="category"]/span[1]').text
                except Exception as e:
                    print("未获得标记人数")
                    print(e)
                #结束循环
                break
            print("查找到的标记remark:%s %s"%(remark,num_remark))
        except Exception as e:
            print("查找异常")
            print(e)
def get_data(baidu):
    while True:
        phone_num = raw_input("请输入手机号：")
        if phone_num=='exit':
            return
        baidu.GetBiaoji(phone_num)

if __name__ == '__main__':
    baidu = Baidu()
    get_data(baidu)
    # phone_num = "13113140381"
    # baidu.GetBiaoji(phone_num)


