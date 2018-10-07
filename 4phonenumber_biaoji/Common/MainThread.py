#coding=utf-8
import sys
sys.path.append('..')
from PlatForm.Baidu import Baidu
from PlatForm.Best114 import Best114
# from PlatForm.dianhuaban import DianHuaBan
from PlatForm.So360 import So360
from PlatForm.Sogo import Sogo
from PlatForm.Baiduhaoma import Baiduhaoma
from PlatForm.Baiduwap import Baiduwap
from PlatForm.Wxguanjia import Wxguanjia
from PlatForm.Wxshouhu import Wxshouhu
import time
import urllib2
import json
import threading
from MyDriver import MyDriver
from PhoneList import phoneList
from common import *

class MainThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.result_data = []
        self.myDriver = MyDriver()
        self.baidu = Baidu()
        self.baiduhaoma = Baiduhaoma()
        self.baiduwap = Baiduwap()
        self.best114 = Best114()
        self.so360 = So360()
        self.sogo = Sogo()
        self.wxguanjia = Wxguanjia()
        self.wxshouhu = Wxshouhu()

        self.status = True
        #数据请求url
        self.get_task_url = "http://ptu.my/api/Psign/get_task?sc=%s"%my_secret#获取任务
        self.update_task_url = "http://ptu.my/api/Psign/update_task"#更新任务

    #线程
    def run(self):
        try:
            log_info("thread main start...")
            # task_status = True #True表示网络查不到任务，需要等待订阅消息，否则表示有任务，需要不断查询网络处理
            while self.status:
                self.result_data = []
                # if task_status and phoneList.isNull():
                #     time.sleep(1)
                #     continue
                # else:#非空，则说明有任务，进行请求
                #     task_status = False
                res = self.get_task()
                if res['code'] != -1:
                    log_info("+++++++++%s+++++++++++"%res['msg'])
                    phone_num = res['data']['p']
                    plat_form = res['data']['f']
                else:
                    log_info("+++++++++%s+++++++++++"%res['msg'])
                    # task_status = True
                    #根据接口返回的睡眠时间进行等待
                    sleep_time = res['st']
                    if sleep_time<=0:
                        sleep_time=1
                    time.sleep(sleep_time)
                    continue
                #查询各个平台的标记情况
                if plat_form == "baidu":
                    result = self.baidu.GetBiaoji(self.myDriver,phone_num)
                elif plat_form == "baiduwap":
                    result = self.baiduwap.GetBiaoji(self.myDriver,phone_num)
                elif plat_form == "baiduhaoma":
                    result = self.baiduhaoma.GetBiaoji(self.myDriver,phone_num)
                elif plat_form == "best114":
                    result = self.best114.GetBiaoji(self.myDriver,phone_num)
                elif plat_form == "so360":
                    result = self.so360.GetBiaoji(self.myDriver,phone_num)
                elif plat_form == "sogo":
                    result = self.sogo.GetBiaoji(self.myDriver,phone_num)
                elif plat_form == "wxguanjia":
                    result = self.wxguanjia.GetBiaoji(self.myDriver,phone_num)
                elif plat_form == "wxshouhu":
                    result = self.wxshouhu.GetBiaoji(self.myDriver,phone_num)
                else:
                    result = "选择平台异常"
                log_info("结束查询,查询结果如下:")
                log_info(result)
                self.update_task(phone_num,plat_form,result)
            #线程结束，浏览器关闭
            self.myDriver.DriverQuit()
            pass
        except Exception as e:
            log_error("Run error:")
            log_error(e)
            try:
                #线程结束，浏览器关闭
                self.myDriver.DriverQuit()
            except Exception as e:
                pass
        log_info("thread main stop...")

    #获取任务
    def get_task(self):
        try:
            res = urllib2.urlopen(self.get_task_url)
            res = res.read()
            return json.loads(res)
        except Exception as e:
            log_error("请求异常")
            log_error(e)
            return {'code':-1,'st':1,'msg':'请求异常'}#st为请求睡眠时间
    #更新任务
    def update_task(self,phone,platform,mark):
        try:
            url = self.update_task_url+"?sc=%s&p=%s&f=%s&m=%s"%(my_secret,phone,platform,mark)
            res = urllib2.urlopen(url)
            res = res.read()
            return json.loads(res)
        except Exception as e:
            log_error("请求异常")
            log_error(e)
            return {'code':-1}
    #停止线程
    def stop_thread(self):
        self.status = False