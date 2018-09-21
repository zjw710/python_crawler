#coding=utf-8
#浏览器初始化类
from selenium import webdriver
from common import *
import time
class MyDriver(object):
    def __init__(self):
        self.driver = None
        self.InitDriver()
        pass
    #初始化浏览器
    def InitDriver(self):
        tag = False
        try:
            #如果driver存在，则退出再创建
            if not self.driver:
                pass
            else:
                self.driver.quit()
        except Exception as e:
            log_error("释放浏览器资源失败")
            log_error(e)
        #创建浏览器对象
        try:
            browser = "firefox"
            if browser == "firefox":
                options = webdriver.FirefoxOptions()
                options.set_headless()#或者使用options.add_argument('-headless')
                options.add_argument('--disable-gpu')#禁用GPU加速
                self.driver = webdriver.Firefox(firefox_options=options)
                self.driver = webdriver.Firefox()
            elif browser == "chrome":
                self.driver = webdriver.Chrome()
            else:
                from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
                dcap = dict(DesiredCapabilities.PHANTOMJS)
                # dcap['phantomjs.page.settings.userAgent'] = ('Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36')
                dcap['phantomjs.page.settings.userAgent'] = ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36')
                self.driver = webdriver.PhantomJS(executable_path=r"./phantomjs",desired_capabilities=dcap,service_args=['--ignore-ssl-errors=true'])
                # self.driver = webdriver.PhantomJS(executable_path = "./phantomjs")
            tag = True
        except Exception as e:
            log_error("打开浏览器异常")
            log_error(e)
        return tag
    def GetDriver(self):
        return self.driver
    def GetUrl(self,url):
        try:
            self.driver.get(url)
            t = int(time.time())#获取秒级时间戳
            img_url = "./screenshot_img/"+str(t)+".png"
            self.driver.save_screenshot(img_url)
            return self.driver
        except Exception as e:
            log_error("GetUrl error:%s"%e)
            return False
