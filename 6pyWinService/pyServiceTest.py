#ZPF
#encoding=utf-8
import win32serviceutil
import win32service
import win32event
import os
import logging
import inspect
class PySerTest(win32serviceutil.ServiceFramework):
    _svc_name_ = "PySerTest"
    _svc_display_name_ = "Py Service Test"
    _svc_description_ = "This is a python service test code "
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.logger = self._getLogger()
        self.run = True
    def _getLogger(self):
        logger = logging.getLogger('[PythonService]')
        this_file = inspect.getfile(inspect.currentframe())
        dirpath = os.path.abspath(os.path.dirname(this_file))
        # handler = logging.FileHandler(os.path.join(dirpath, "service.log"))
        handler = logging.FileHandler("G:\\service.log")
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger
    def SvcDoRun(self):
        import time
        self.logger.info("service is run....")
        while self.run:
            self.logger.info("I am runing....")
            time.sleep(2)

    def SvcStop(self):
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