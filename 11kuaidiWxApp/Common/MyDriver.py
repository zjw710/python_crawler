#coding=utf-8
#浏览器初始化类
from selenium import webdriver
from common import *
import time
from selenium.common.exceptions import TimeoutException
class MyDriver(object):
    def __init__(self):
        self.driver = None
        self.status = self.InitDriver()
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
            browser = my_browser
            if browser == "firefox":
                options = webdriver.FirefoxOptions()
                if my_sys_platform=="Linux":
                    options.set_headless()#或者使用options.add_argument('-headless')
                options.add_argument('--disable-gpu')#禁用GPU加速

                firefox_profile = webdriver.FirefoxProfile()
                user_agent = get_header()#随机user_agent
                my_log.logger.info("get random user_agent:%s"%user_agent)
                firefox_profile.set_preference("general.useragent.override", user_agent)
                #如果要截图，则加载图片，否则不加载
                if is_screenshot != '1':
                    firefox_profile.set_preference('permissions.default.image', 2)#禁止加载图片，某些firefox只需要这个
                firefox_profile.update_preferences()
                # firefox_profile.set_preference('browser.migration.version', 9001)#禁止加载图片，部分需要加上这个
                # firefox_profile.set_preference('permissions.default.stylesheet', 2)#禁用css
                # firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')#禁用flash
                # firefox_profile.set_preference('javascript.enabled', 'false')#禁用js
                if my_sys_platform=="Linux":
                    self.driver = webdriver.Firefox(executable_path="./geckodriver",firefox_profile=firefox_profile,firefox_options=options)
                else:
                    self.driver = webdriver.Firefox(firefox_profile=firefox_profile,firefox_options=options)
                # self.driver = webdriver.Firefox()
            elif browser == "chrome":

                # WIDTH = 320
                # HEIGHT = 640
                # PIXEL_RATIO = 3.0
                # UA = 'Mozilla/5.0 (Linux; Android 4.1.1; GT-N7100 Build/JRO03C) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/35.0.1916.138 Mobile Safari/537.36 T7/6.3'
                # mobileEmulation = {"deviceMetrics": {"width": WIDTH, "height": HEIGHT, "pixelRatio": PIXEL_RATIO}, "userAgent": UA}
                # options = webdriver.ChromeOptions()
                # options.add_experimental_option('mobileEmulation', mobileEmulation)
                # self.driver = webdriver.Chrome(chrome_options=options)
                # prefs = {"profile.managed_default_content_settings.images": 2}#禁止加载图片
                # options.add_experimental_option("prefs", prefs)
                self.driver = webdriver.Chrome()

            elif browser == "ie":
                self.driver = webdriver.Ie()
            elif browser == "phantomjs":
                from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
                dcap = dict(DesiredCapabilities.PHANTOMJS)
                # dcap['phantomjs.page.settings.userAgent'] = ('Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36')
                dcap['phantomjs.page.settings.userAgent'] = ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36')
                self.driver = webdriver.PhantomJS(executable_path=r"./phantomjs",desired_capabilities=dcap,service_args=['--ignore-ssl-errors=true'])
                # self.driver = webdriver.PhantomJS(executable_path = "./phantomjs")
            else:
                self.driver = webdriver.Firefox()
            #设置请求超时时间
            self.driver.set_page_load_timeout(5)
            self.driver.set_script_timeout(5)
            tag = True
            log_info("打开浏览器成功Open browser successfully")
        except Exception as e:
            log_error("打开浏览器异常Failed to open browser")
            log_error(e)
            tag = False
        return tag
    def GetDriver(self):
        return self.driver
    def GetUrl(self,url):
        try_num = 1
        max_try_num = 3
        #由于访问一个页面后，再访问一次会失败，因此需要多次尝试，最多尝试3次
        while True:
            try:
                if try_num >= max_try_num:
                    break
                self.driver.get(url)
                return self.driver
            except TimeoutException as e:#处理超时问题
                my_log.logger.info(e)
                return self.driver
            except Exception as e:
                log_error("GetUrl error:%s,try again"%e)
                try_num += 1
                time.sleep(1)
        return False
    #退出浏览器
    def DriverQuit(self):
        self.driver.quit()
    #截图
    #type 如果为error,则表示异常
    def ScreenShot(self,phone,type=""):
        #是否截图
        if is_screenshot == '1':
            timestruct = time.localtime(time.time())
            path = time.strftime('%Y%m%d', timestruct)+type
            screenshot_path = os.path.join(my_dirpath,"./screenshot_img/"+path+"/")
            # my_log.logger.info(path)
            # my_log.logger.info(screenshot_path)
            check_path(screenshot_path)
            t = int(time.time())#获取秒级时间戳
            img_url = screenshot_path+str(t)+"_"+phone+".png"
            # my_log.logger.info(img_url)
            self.driver.save_screenshot(img_url)

if __name__ == '__main__':
    my_driver = MyDriver()
    driver = my_driver.GetDriver()
    driver.get("https://httpbin.org/get?show_env=1")
    html = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
    my_log.logger.info(html)
    print("sleep 10s")
    time.sleep(10)
    driver.close()
