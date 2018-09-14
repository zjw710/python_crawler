#coding=utf-8
#手机号标记查询
from selenium import webdriver
class Best114(object):
    def __init__(self):
        self.url = "http://www.114best.com/dh/114.aspx?w=13800138006"
        self.baseUrl = "http://www.114best.com"
        pass
    def GetBiaoji(self,phone_num):
        driver = webdriver.Firefox()
        try:
            driver.get(self.url)
            search_input = driver.find_element_by_id("w")
        except:
            print("服务器异常")
            return
        search_input.clear()
        search_input.send_keys(phone_num)

        search_btn = driver.find_element_by_id("query")
        search_btn.click()
        try:
            tag_Name = driver.find_element_by_xpath('//*[@id="tag_Name"]/img')
            tag_url = tag_Name.get_attribute("src")
        except:
            tag_url = "无标记"
        print(tag_url)
if __name__ == '__main__':
    best = Best114()
    phone_num = "13113140381"
    best.GetBiaoji(phone_num)


