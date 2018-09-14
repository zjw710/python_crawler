#coding=utf-8
#手机号标记查询
from selenium import webdriver
import time
from PIL import Image
class dianhua(object):
    def __init__(self):
        self.key = "13800138006"
        self.url = "http://www.dianhua.cn/search/dongguan?key="+self.key
        pass
    def GetBiaoji(self,phone_num):
        driver = webdriver.Firefox()
        driver.get(self.url)
        try:
            while True:
                identify_code = driver.find_element_by_id("captcha")
                print("需要等待输入验证码")
                time.sleep(5)
                screen_img_url = "./screenshot_img/"+self.key+".png"
                driver.save_screenshot(screen_img_url)
                code_pos = identify_code.location#获取图片验证码坐标
                code_size = identify_code.size#获取图片验证码的大小
                code_rangle = (int(code_pos['x']), int(code_pos['y']), int(code_pos['x'] + code_size['width']),
                               int(code_pos['y'] + code_size['height']))  # 写成我们需要截取的位置坐标
                screen_img = Image.open(screen_img_url)
                code_img = screen_img.crop(code_rangle)
                t = int(time.time())#获取秒级时间戳
                code_img_url = "./code_img/"+self.key+"_"+str(t)+".png"
                code_img.save(code_img_url)
                print("生成验证码："+code_img_url)
                identify_code.click()#点击验证码，用于采集验证码图片
        except Exception as e:
            print("无需验证码")
            print(e)

        try:
            print("等待2s...")
            time.sleep(2)
            tag = driver.find_element_by_xpath('//*[@class="c_right_list"]/dl/dt/h5/a').text
            print("找到标记如下：")
            print("tag:"+tag)
            tag_url = driver.find_element_by_xpath('//*[@class="c_right_list"]/dl/dt/h5/a').get_attribute("href")
            print("tag_url:"+tag_url)
        except:
            print("找不到标记")

if __name__ == '__main__':
    best = dianhua()
    phone_num = "13113140381"
    best.GetBiaoji(phone_num)


