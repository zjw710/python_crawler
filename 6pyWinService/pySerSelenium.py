#ZPF
#encoding=utf-8
import win32serviceutil
import win32service
import win32event
import logging
import inspect
from selenium import webdriver
import  os
import sys
this_file = inspect.getfile(inspect.currentframe())

#判断是脚本还是exe文件，获取工作目录真实路径
def cur_file_dir():
    #获取脚本路径
    path = os.path.realpath(__file__)
    #判断为脚本文件还是pyinstaller编译后的文件，如果是脚本文件，则返回的是脚本的目录，
    if os.path.exists(path):#如果路径存在，则是脚本文件
        return sys.path[0]
    else:#否则为编译后的exe文件
        return os.path.dirname(os.path.realpath(sys.argv[0]))
#判断路径是否存在，否则创建
def check_path(filename):
    #将文件路径分割出来
    file_dir = os.path.split(filename )[0]
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)
#获取路径
dirpath = cur_file_dir()

class PySerTest(win32serviceutil.ServiceFramework):
    _svc_name_ = "PySerSelenium"
    _svc_display_name_ = "Py Service Selenium"
    _svc_description_ = "This is a python service test code "
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.logger = self._getLogger()
        # phantomjspath = os.path.join(dirpath, "./phantomjs.exe")
        # self.driver = webdriver.PhantomJS(executable_path = phantomjspath)
        browser = "firefox"
        if browser == "firefox":
            self.driver = webdriver.Firefox()
        else:
            from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap['phantomjs.page.settings.userAgent'] = ('Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36')
            phantomjspath = os.path.join(dirpath, "./phantomjs.exe")
            self.driver = webdriver.PhantomJS(executable_path=phantomjspath,desired_capabilities=dcap,service_args=['--ignore-ssl-errors=true'])
        self.run = True
    def _getLogger(self):
        logger = logging.getLogger('[PythonService]')
        log_path = os.path.join(dirpath, "./log/service.log")
        check_path(log_path)
        handler = logging.FileHandler(log_path)
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger


    def SvcDoRun(self):
        import time
        self.logger.info("service is run....")

        while self.run:
            try:
                self.driver.get('http://service.spiritsoft.cn/ua.html')
                t = int(time.time())#获取秒级时间戳
                img_url = "./img/test_"+str(t)+".png"
                img_url = os.path.join(dirpath, img_url)
                check_path(img_url)
                # img_url = "D:\\phantomjs\\"+img_url
                self.logger.info(img_url)
                self.driver.save_screenshot(img_url)
                self.logger.info("I am runing....")
            except Exception as e:
                self.logger.info("I am exception....")
                self.logger.info(e)
            time.sleep(5)

    def SvcStop(self):
        self.driver.quit()
        self.logger.info("service is stop....")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)
        self.run = False
if __name__=='__main__':
    # win32serviceutil.HandleCommandLine(PythonService)
    import sys
    import servicemanager
    if len(sys.argv) == 1:
        try:
            evtsrc_dll = os.path.abspath(servicemanager.__file__)
            servicemanager.PrepareToHostSingle(PySerTest) #如果修改过名字，名字要统一
            servicemanager.Initialize('PySerTest',evtsrc_dll) #如果修改过名字，名字要统一
            servicemanager.StartServiceCtrlDispatcher()
        except win32service.error as details:
            import winerror
            if details == winerror.ERROR_FAILED_SERVICE_CONTROLLER_CONNECT:
                win32serviceutil.usage()
    else:
        win32serviceutil.HandleCommandLine(PySerTest) #如果修改过名字，名字要统一