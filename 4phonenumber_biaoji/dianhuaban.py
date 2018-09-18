#coding=utf-8
#手机号标记查询
from selenium import webdriver
import time
from PIL import Image

import sys
# from ShowapiRequest import ShowapiRequest
from CodeApi.ShowapiRequest import ShowapiRequest
import base64
reload(sys)
sys.setdefaultencoding('utf-8')
class dianhua(object):
    def __init__(self):
        #测试电话：076922762885 ， 13800138006 ，18122363191 ， 02039999993
        self.key = "13800138006"
        self.url = "http://www.dianhua.cn/search/dongguan?key="
        self.driver = webdriver.Firefox()
        pass
    #将图片验证码转成base64格式
    def GetBase64(self,img_url):
        try:
            f=open(img_url,'rb') #二进制方式打开图文件
            ls_f="data:image/jpeg;base64,"+base64.b64encode(f.read()) #读取文件内容，转换为base64编码
            f.close()
            print("转base64成功:"+ls_f)
            return ls_f
        except Exception as e:
            print("转base64失败:"+img_url)
            print(e)
            return 'error'

    #识别图片验证码
    def IdentifyCode(self,img_url):
        try:
            base64_img = self.GetBase64(img_url)
            if base64_img=='error':
                return 'error'
            r = ShowapiRequest("http://route.showapi.com/184-2","75245","5071c4914036439c8d1df67484d773b2" )
            r.addBodyPara("typeId", "50")
            r.addBodyPara("convert_to_jpg", "0")
            r.addBodyPara("img_base64", base64_img) #文件上传时设置
            res = r.post()
            print("验证码解析结果:"+res.text) # 返回信息
            res = res.json()
            if res['showapi_res_code'] != 0:
                print("识别验证码失败")
                return 'error'
            result = res['showapi_res_body']['Result']
            return result
        except Exception as e:
            print("识别验证码失败")
            print(e)
            return 'error'
        pass
    def GetBiaoji(self,phone_num):
        driver = self.driver
        try:
            driver.get(self.url+phone_num)
        except Exception as e:
            print("浏览器异常,重新打开浏览器")
            print(e)
            try:
                self.driver = webdriver.Firefox()
                driver = self.driver
                driver.get(self.url+phone_num)
            except Exception as e:
                print("重新打开浏览器异常，不再尝试")
                print(e)
                return
        summit_times = 0#检查验证码次数，如果2次失败就不再尝试
        try:
            while True:
                time.sleep(1)
                identify_code = driver.find_element_by_id("captcha")
                if summit_times>2:
                    print("验证码错误2次以上，不再进行进行尝试...")
                    return
                elif summit_times>0:
                    print("验证码错误%s次，重新输入验证码..."%summit_times)
                else:
                    print("等待输入验证码...")
                #裁切获取验证码图片
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
                print("生成验证码图片："+code_img_url)
                # identify_code.click()#点击验证码，用于采集验证码图片
                #识别验证码
                auto_check = 0#是否自动识别验证码
                if auto_check == 0:
                    code = raw_input("请输入验证码:")
                else:#自动识别验证码
                    code = self.IdentifyCode(code_img_url)
                    if code=='error':
                        code = raw_input("自动识别验证码异常，请手动输入验证码:")

                code = code.decode('utf-8')#由于有中文，因此进行转义
                #提交验证码
                code_input = driver.find_element_by_name("code")
                code_input.send_keys(code)

                summit_btn = driver.find_element_by_xpath('//*[@class="error_guide"]/form/p/input[2]')
                summit_btn.click()
                #提交次数
                summit_times += 1

        except Exception as e:
            print("无需验证码")
            print(e)

        try:
            print("等待1s...")
            time.sleep(1)
            tag = driver.find_element_by_xpath('//*[@class="c_right_list"]/dl/dt/h5/a').text
            print("找到标记如下：")
            print("tag:"+tag)
            tag_url = driver.find_element_by_xpath('//*[@class="c_right_list"]/dl/dt/h5/a').get_attribute("href")
            print("tag_url:"+tag_url)
        except:
            print("找不到标记")

def get_data(best):
    while True:
        phone_num = raw_input("请输入手机号：")
        if phone_num=='exit':
            return
        best.GetBiaoji(phone_num)

if __name__ == '__main__':
    best = dianhua()
    get_data(best)
    # phone_num = "13113140381"
    # best.GetBiaoji(phone_num)


