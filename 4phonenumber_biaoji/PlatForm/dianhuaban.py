#coding=utf-8
#电话邦查询
#13800138006 ，18122363191 ， 02039999993 ， 17640298760
from selenium import webdriver
import sys
sys.path.append('..')
from Common.MyDriver import MyDriver
from Common.common import *
import time
from PIL import Image
# from ShowapiRequest import ShowapiRequest
from CodeApi.ShowapiRequest import ShowapiRequest
import base64
reload(sys)
sys.setdefaultencoding('utf-8')
class DianHuaBan(object):
    def __init__(self):
        #测试电话：076922762885 ， 13800138006 ，18122363191 ， 02039999993
        self.key = "13800138006"
        self.url = "http://www.dianhua.cn/search/dongguan?key="
        pass
    #将图片验证码转成base64格式
    def GetBase64(self,img_url):
        try:
            f=open(img_url,'rb') #二进制方式打开图文件
            ls_f="data:image/jpeg;base64,"+base64.b64encode(f.read()) #读取文件内容，转换为base64编码
            f.close()
            LogInfoDianHuaBan("转base64成功:"+ls_f)
            return ls_f
        except Exception as e:
            LogInfoDianHuaBan("转base64失败:"+img_url)
            LogInfoDianHuaBan(e)
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
            LogInfoDianHuaBan("验证码解析结果:"+res.text) # 返回信息
            res = res.json()
            if res['showapi_res_code'] != 0:
                LogInfoDianHuaBan("识别验证码失败")
                return 'error'
            result = res['showapi_res_body']['Result']
            return result
        except Exception as e:
            LogInfoDianHuaBan("识别验证码失败")
            LogInfoDianHuaBan(e)
            return 'error'
        pass
    def GetBiaoji(self,myDriver,phone_num):
        url = self.url+phone_num
        driver = myDriver.GetUrl(url)
        if not driver:
            LogErrorDianHuaBan(u"浏览器异常，查询结束")
            return
        summit_times = 0#检查验证码次数，如果2次失败就不再尝试
        try:
            code = 0
            remark = tip_img =""
            while True:
                time.sleep(1)
                identify_code = driver.find_element_by_id("captcha")
                if summit_times>2:
                    LogInfoDianHuaBan("验证码错误2次以上，不再进行进行尝试...")
                    return
                elif summit_times>0:
                    LogInfoDianHuaBan("验证码错误%s次，重新输入验证码..."%summit_times)
                else:
                    LogInfoDianHuaBan("等待输入验证码...")
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
                LogInfoDianHuaBan("生成验证码图片："+code_img_url)
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
            LogInfoDianHuaBan("无需验证码")
            LogInfoDianHuaBan(e)

        try:
            LogInfoDianHuaBan("等待1s...")
            time.sleep(1)
            remark = driver.find_element_by_xpath('//*[@class="c_right_list"]/dl/dt/h5/a').text
            LogInfoDianHuaBan("找到标记如下：")
            LogInfoDianHuaBan("tag:"+remark)
            tip_img = driver.find_element_by_xpath('//*[@class="c_right_list"]/dl/dt/h5/a').get_attribute("href")
            LogInfoDianHuaBan("tag_url:"+tip_img)
            code = 1
        except:
            LogInfoDianHuaBan("找不到标记")
        result = {"type":"Dianhuaban","code":code,"remark":remark,"tip_img":tip_img}
        return result

def get_data(dianhuaban):
    myDriver = MyDriver()
    while True:
        phone_num = raw_input("请输入手机号：")
        if phone_num=='exit':
            return
        result = dianhuaban.GetBiaoji(myDriver,phone_num)
        LogInfoDianHuaBan(result)
def LogInfoDianHuaBan(str):
    log_info("[Baidu]%s"%str)
def LogErrorDianHuaBan(str):
    log_error("[Baidu]%s"%str)
if __name__ == '__main__':
    dianhuaban = DianHuaBan()
    get_data(dianhuaban)


