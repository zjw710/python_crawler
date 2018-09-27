# #coding=utf-8
# #汇总所有查询平台
#encoding=utf-8
import win32serviceutil
import win32service
import win32event
from selenium import webdriver
from Common.common import *
from Common.MyRedisThread import MyRedisThread
from Common.MainThread import MainThread

#获取路径
dirpath = cur_file_dir()
class PySerTest(win32serviceutil.ServiceFramework):
    _svc_name_ = "PyCheckPhone"
    _svc_display_name_ = "Py CheckPhone"
    _svc_description_ = "This is a python service checkPhone"
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.run = True

    def SvcDoRun(self):
        try:
            log_info("service start...")
            self.thread1 = MainThread()
            channel = 'phonemark'
            self.thread2 = MyRedisThread(channel)

            self.thread1.start()
            self.thread2.start()

            self.thread1.join()
            self.thread2.join()
        except Exception as e:
            log_error("main error:")
            log_error(e)

    def SvcStop(self):
        log_info("service stop...")
        self.thread1.stop_thread()
        self.thread2.stop_thread()
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