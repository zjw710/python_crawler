#coding=utf-8
#汇总所有查询平台
#13800138006 ，18122363191 ， 02039999993 ， 17640298760 ，076922762885
from Common.MyDriver import MyDriver
from Common.common import *
from Baidu import Baidu
from Best114 import Best114
from dianhuaban import DianHuaBan
from So360 import So360
from Sogo import Sogo
from Common.MyRedis import MyRedisThread
import threading
import time
from Common.PhoneList import phoneList
class MainThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.result_data = []
        self.myDriver = MyDriver()
        self.baidu = Baidu()
        self.best114 = Best114()
        self.so360 = So360()
        self.sogo = Sogo()
        self.status = True
    #线程
    def run(self):
        try:
            print("thread main start...")
            while self.status:
                self.result_data = []
                # phone_num = raw_input("请输入手机号：")
                # if phone_num=='exit':
                #     self.myDriver.driver.quit()
                #     return
                phone_num = phoneList.isNull()
                print("phone_num:%s"%phone_num)
                if not phone_num:
                    time.sleep(5)
                    continue

                baidu_data = self.baidu.GetBiaoji(self.myDriver,phone_num)
                self.result_data.append(baidu_data)
                best114_data = self.best114.GetBiaoji(self.myDriver,phone_num)
                self.result_data.append(best114_data)
                so360_data = self.so360.GetBiaoji(self.myDriver,phone_num)
                self.result_data.append(so360_data)
                sogo_data = self.sogo.GetBiaoji(self.myDriver,phone_num)
                self.result_data.append(sogo_data)
                log_info("结束查询,查询结果如下:")
                log_info(self.result_data)
            pass
        except Exception as e:
            log_error("Run error:")
            log_error(e)

if __name__ == '__main__':
    try:
        thread1 = MainThread()
        channel = 'test'
        thread2 = MyRedisThread(channel)

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()
        # biaoji = BaseChaBiaoji()
        # biaoji.Run()
    except Exception as e:
        log_error("main error:")
        log_error(e)
