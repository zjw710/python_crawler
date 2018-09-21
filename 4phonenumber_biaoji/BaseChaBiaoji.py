#coding=utf-8
#汇总所有查询平台
#13800138006 ，18122363191 ， 02039999993 ， 17640298760 ，076922762885
from Common.MyDriver import MyDriver
from Common.common import *
from PlatForm.Baidu import Baidu
from PlatForm.Best114 import Best114
from PlatForm.dianhuaban import DianHuaBan
from PlatForm.So360 import So360
from PlatForm.Sogo import Sogo
from Common.MyRedisThread import MyRedisThread
import threading
import time
import urllib2
import json
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
        #数据请求url
        self.get_task_url = "http://127.0.0.1:1001/api/Phonesign/get_task"#获取任务
        self.update_task_url = "http://127.0.0.1:1001/api/Phonesign/update_task"#更新任务

    #线程
    def run(self):
        try:
            print("thread main start...")
            task_status = True #True表示网络查不到任务，需要等待订阅消息，否则表示有任务，需要不断查询网络处理
            while self.status:
                self.result_data = []
                # phone_num = raw_input("请输入手机号：")
                # if phone_num=='exit':
                #     self.myDriver.driver.quit()
                #     return
                # print("phone_num:%s"%phone_num)
                if task_status and phoneList.isNull():
                    time.sleep(5)
                    continue
                else:#非空，则说明有任务，进行请求
                    task_status = False
                    res = self.get_task()
                    if res['code'] != -1:
                        log_info("+++++++++接收到任务+++++++++++")
                        phone_num = res['data']['p']
                        plat_form = res['data']['f']
                    else:
                        log_info("+++++++++查询不到任务+++++++++++")
                        task_status = True
                        continue
                #查询各个平台的标记情况
                if plat_form == "baidu":
                    result = self.baidu.GetBiaoji(self.myDriver,phone_num)
                elif plat_form == "best114":
                    result = self.best114.GetBiaoji(self.myDriver,phone_num)
                elif plat_form == "so360":
                    result = self.so360.GetBiaoji(self.myDriver,phone_num)
                elif plat_form == "sogo":
                    result = self.sogo.GetBiaoji(self.myDriver,phone_num)
                else:
                    result = "选择平台异常"
                log_info("结束查询,查询结果如下:")
                log_info(result)
                self.update_task(phone_num,plat_form,result)
            pass
        except Exception as e:
            log_error("Run error:")
            log_error(e)
    #获取任务
    def get_task(self):
        try:
            res = urllib2.urlopen(self.get_task_url)
            res = res.read()
            return json.loads(res)
        except Exception as e:
            log_error("请求异常")
            log_error(e)
            return {'code':-1}
    #更新任务
    def update_task(self,phone,platform,mark):
        try:
            url = self.update_task_url+"?p=%s&f=%s&m=%s"%(phone,platform,mark)
            res = urllib2.urlopen(url)
            res = res.read()
            return json.loads(res)
        except Exception as e:
            log_error("请求异常")
            log_error(e)
            return {'code':-1}

if __name__ == '__main__':
    try:
        thread1 = MainThread()
        channel = 'phonemark'
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
